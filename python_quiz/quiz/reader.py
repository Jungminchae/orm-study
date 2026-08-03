import json
from importlib.resources import files

from rich import print

from python_quiz.quiz.constants import CHAPTER


def get_chapter(chapter_number: str, _type: str = "1", is_exam: bool = False) -> list[dict]:
    """
    get quiz from quiz JSON file.

    :param chapter_number: chapter_number ∈ CHAPTER
    :param _type: _type ∈ TYPE (1: 객관식, 2: 주관식, 3: 혼합)
    :param is_exam: True if exam mode
    :return: List of quiz dictionaries
    """
    chapter_name = CHAPTER.get(chapter_number)
    quiz_path = f"python_quiz.quiz._python.{chapter_name}"

    if not chapter_name:
        raise ValueError(f"Invalid chapter number: {chapter_number}")

    json_path = files(quiz_path).joinpath("quiz.json")
    try:
        with open(json_path, encoding="utf-8") as f:
            quizzes = json.load(f)
    except FileNotFoundError:
        return []

    filtered = []
    has_subjective = False

    for q in quizzes:
        if q.get("type") == "multiple_choice":
            if _type in ("1", "3"):
                filtered.append(q)
        elif q.get("type") == "subjective":
            has_subjective = True
            if _type in ("2", "3"):
                filtered.append(q)

    if _type == "2" and not has_subjective:
        if not is_exam:
            print("[red bold]주관식 문제가 없습니다. \n객관식 문제만 출제합니다.ㅠㅠ")
        for q in quizzes:
            if q.get("type") == "multiple_choice":
                filtered.append(q)

    elif _type == "3" and not has_subjective:
        if not is_exam:
            print("[red bold]주관식 문제가 없습니다. \n객관식 문제만 출제합니다.ㅠㅠ")

    return filtered


def parse_content(quizzes: list[dict]) -> tuple[list[str], list[str]]:
    formatted_quizzes = []
    answers = []

    for q in quizzes:
        question_text = f"\n.{q['question']}\n\n"
        if q.get("type") == "multiple_choice" and q.get("options"):
            for i, opt in enumerate(q["options"], 1):
                question_text += f"{i}. {opt}\n"

        formatted_quizzes.append(question_text.rstrip())
        answers.append(str(q["answer"]).strip())

    return formatted_quizzes, answers
