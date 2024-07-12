import pytest
import typer
from typer.testing import CliRunner
from orm_study.quiz.command import select_chapter, select_quiz_type, fetch_quiz, select_quiz_num, solve_quiz, display_results
from orm_study.quiz.constants import CHAPTER, CHAPTER_CHOICE, TYPE_CHOICE
from orm_study.main import app

runner = CliRunner()


@pytest.fixture
def mock_chapters(monkeypatch):
    monkeypatch.setattr("orm_study.quiz.constants.CHAPTER", CHAPTER)
    monkeypatch.setattr("orm_study.quiz.constants.CHAPTER_CHOICE", CHAPTER_CHOICE)
    monkeypatch.setattr("orm_study.quiz.constants.TYPE_CHOICE", TYPE_CHOICE)


def test_select_chapter_valid(monkeypatch, mock_chapters):
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda prompt: "1")
    assert select_chapter() == "1"


def test_select_chapter_invalid(monkeypatch, mock_chapters):
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda prompt: "333")
    with pytest.raises(typer.Exit):
        select_chapter()


def test_select_quiz_type_valid(monkeypatch):
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda prompt, choices: "1")
    assert select_quiz_type() == "1"


def test_select_quiz_type_invalid(monkeypatch):
    inputs = iter(["4", "2"])
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda prompt, choices: next(inputs))
    assert select_quiz_type() == "2"


def test_select_quiz_num_valid(monkeypatch):
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda prompt: "3")
    assert select_quiz_num(5) == 3


def test_select_quiz_num_exceeding(monkeypatch):
    inputs = iter(["6", "4"])  # 첫 번째 입력이 초과, 두 번째 입력은 유효
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda prompt: next(inputs))
    assert select_quiz_num(5) == 4


def test_fetch_quiz(monkeypatch):
    def mock_get_chapter(chapter_number: str):
        return "Quiz 1\nAnswer 1\nQuiz 2\nAnswer 2"

    def mock_parse_content(quiz_txt: str):
        return ["Quiz 1", "Quiz 2"], ["Answer 1", "Answer 2"]

    monkeypatch.setattr("orm_study.quiz.command.get_chapter", mock_get_chapter)
    monkeypatch.setattr("orm_study.quiz.command.parse_content", mock_parse_content)

    quiz_answer_set = fetch_quiz("1", "1")
    assert len(quiz_answer_set) == 2


def test_solve_quiz(monkeypatch):
    inputs = iter(["Answer 1", "Wrong Answer"])
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda prompt: next(inputs))

    quiz_answer_set = [("Quiz 1", "Answer 1"), ("Quiz 2", "Answer 2")]
    results = solve_quiz(quiz_answer_set)
    assert results == [True, False]


def test_display_results(capfd):
    user_answers = [True, False, True]
    display_results("1", user_answers)

    captured = capfd.readouterr()
    assert "챕터 1 퀴즈 결과" in captured.out
    assert "총 3문제 중 2문제를 맞추셨습니다." in captured.out


def test_start(monkeypatch):
    inputs = iter(["1", "1", "1", "Answer 1"])
    monkeypatch.setattr("rich.prompt.Prompt.ask", lambda prompt, choices=None: next(inputs))  # choices 추가

    monkeypatch.setattr("orm_study.quiz.command.fetch_quiz", lambda chapter, type: [("Quiz 1", "Answer 1")])
    monkeypatch.setattr("orm_study.quiz.command.display_results", lambda chapter, user_answers: None)

    result = runner.invoke(app, ["quiz", "start"])
    assert result.exit_code == 0
