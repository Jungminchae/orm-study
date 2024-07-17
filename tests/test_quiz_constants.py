import os
from orm_study.quiz.constants import CHAPTER, CHAPTER_CHOICE


CHAPTER_DIRS = os.listdir("orm_study/quiz/_python")


def test_check_chapters_all_set() -> None:
    if "__pycache__" in CHAPTER_DIRS:
        CHAPTER_DIRS.remove("__pycache__")

    chapter_lens = len(CHAPTER_DIRS)
    chapter_constants_lens = len(CHAPTER.keys())
    chapter_count_in_choice = CHAPTER_CHOICE.count("챕터")
    assert chapter_lens == chapter_constants_lens == chapter_count_in_choice
