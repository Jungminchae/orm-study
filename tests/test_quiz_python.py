import pytest
from orm_study.quiz.python import PythonQuizSelector, PythonQuizManager, PythonQuiz


def test_quiz_selector_show() -> None:
    selector = PythonQuizSelector()
    selector.show()
    assert True


def test_select_quiz_by_chapter() -> None:
    selector = PythonQuizSelector()
    python_quiz = selector.select_quiz_by_chapter(1, 1)
    assert python_quiz.chapter == "1"


def test_select_quiz_by_chapter_invalid_chapter():
    selector = PythonQuizSelector()
    with pytest.raises(ValueError, match="존재하지 않는 챕터입니다."):
        selector.select_quiz_by_chapter(99, 1)


def test_quiz_manager() -> None:
    python_quiz = PythonQuiz(chapter="1", quiz_list=["Quiz 1", "Quiz 2"])
    manager = PythonQuizManager(python_quiz)
    assert manager.python_quiz.chapter == "1"
    assert manager.python_quiz.quiz_list == ["Quiz 1", "Quiz 2"]
