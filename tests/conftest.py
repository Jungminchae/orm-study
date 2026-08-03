import pytest

from python_quiz.quiz.constants import CHAPTER, CHAPTER_CHOICE, TYPE_CHOICE


@pytest.fixture
def mock_chapters(monkeypatch):
    monkeypatch.setattr("python_quiz.quiz.constants.CHAPTER", CHAPTER)
    monkeypatch.setattr("python_quiz.quiz.constants.CHAPTER_CHOICE", CHAPTER_CHOICE)
    monkeypatch.setattr("python_quiz.quiz.constants.TYPE_CHOICE", TYPE_CHOICE)
