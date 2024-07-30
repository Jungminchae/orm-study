import pytest

from orm_study.quiz.constants import CHAPTER, CHAPTER_CHOICE, TYPE_CHOICE


@pytest.fixture
def mock_chapters(monkeypatch):
    monkeypatch.setattr("orm_study.quiz.constants.CHAPTER", CHAPTER)
    monkeypatch.setattr("orm_study.quiz.constants.CHAPTER_CHOICE", CHAPTER_CHOICE)
    monkeypatch.setattr("orm_study.quiz.constants.TYPE_CHOICE", TYPE_CHOICE)
