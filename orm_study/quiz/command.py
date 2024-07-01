import typer
from typer import Typer
from rich.prompt import Prompt
from rich.panel import Panel
from rich import print
from quiz.constants import CHAPTER, CHAPTER_CHOICE, TYPE_CHOICE

app = Typer()


@app.command()
def start():
    print(Panel(CHAPTER_CHOICE, title="챕터 선택", title_align="center"))
    user_input = Prompt.ask("[white bold]도전할 문제의 챕터를 선택해주세요 ")

    if user_input not in CHAPTER:
        print("[red bold]존재하지 않는 챕터입니다.")
        raise typer.Exit()
    print(Panel(TYPE_CHOICE, title="문제 유형 선택", title_align="center"))
