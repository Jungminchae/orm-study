from importlib import resources  # noqa F401
from quiz.constants import CHAPTER, MULTIPLE, SUBJECTIVE


def get_chapter(chapter_number: str, _type="1") -> str | tuple[str, str]:
    chapter_name = CHAPTER.get(chapter_number)
    quiz_path = f"quiz.python.{chapter_name}"
    if _type == "1":
        with resources.path(quiz_path, MULTIPLE) as quiz_path:
            with open(quiz_path) as multiple_file:
                return multiple_file.read()
    elif _type == "3":
        with resources.path(quiz_path, MULTIPLE) as multiple_path:
            with open(multiple_path) as multiple_file:
                multiple = multiple_file.read()

        with resources.path(quiz_path, SUBJECTIVE) as subjective_path:
            with open(subjective_path) as subjective_file:
                subjective = subjective_file.read()
        return multiple, subjective
    else:
        with resources.path(quiz_path, SUBJECTIVE) as subjective_path:
            with open(subjective_path) as subjective_file:
                return subjective_file.read()


def parse_content(contents: str) -> tuple[list[str], list[str]]:
    quizes = []
    answers = []

    contents = contents.split("---")[:-1]
    for content in contents:
        quiz, answer = content.split("답.")
        quizes.append(quiz.lstrip())
        answers.append(answer.replace("\n", ""))
    return quizes, answers
