import random
import typer
from typer import Typer
from rich.prompt import Prompt
from rich.panel import Panel
from rich import print
from quiz.constants import CHAPTER, CHAPTER_CHOICE, TYPE_CHOICE
from quiz.reader import get_chapter, parse_content

app = Typer()


@app.command()
def start():
    print(Panel(CHAPTER_CHOICE, title="챕터 선택", title_align="center"))
    chapter_input = Prompt.ask("[white bold]도전할 문제의 챕터를 선택해주세요 ")

    if chapter_input not in CHAPTER:
        print("[red bold]존재하지 않는 챕터입니다.")
        raise typer.Exit()
    print(Panel(TYPE_CHOICE, title="문제 유형 선택", title_align="center"))

    while True:
        type_input = Prompt.ask("[white bold]도전할 문제의 유형을 선택해주세요 ", choices=["1", "2", "3"])
        if type_input not in ["1", "2", "3"]:
            print("[red bold]존재하지 않는 유형입니다.")
        else:
            break

    if type_input == "1":
        quiz_txt = get_chapter(chapter_number=chapter_input)
        quizes, answers = parse_content(quiz_txt)
        quiz_answer_set = list(zip(quizes, answers))
        random.shuffle(quiz_answer_set)

    while True:
        quiz_num = Prompt.ask(f"[white bold]문항 수를 선택해주세요. (최대{len(quizes)}개)")
        if not quiz_num:
            quiz_num = len(quizes)
            break
        elif int(quiz_num) > len(quizes):
            print("[red bold]최대 문항 수를 넘을 수 없습니다.ㅠㅠ")
        else:
            break

    print(f"[green bold]챕터 {chapter_input}: {CHAPTER[chapter_input]}\n")
    quiz_answer_set = quiz_answer_set[: int(quiz_num)]
    user_answers = []
    for i, (quiz, answer) in enumerate(quiz_answer_set, start=1):
        print(Panel(f"[blue bold]문제 {i}" + quiz, title_align="center"))
        user_input = Prompt.ask("[white bold] 정답을 입력해주세요: ")
        user_answers.append(user_input == answer)
        print()

    print(f"[green bold]챕터 {chapter_input} 퀴즈 결과")
    print(f"[blue bold]총 {len(quiz_answer_set)}문제 중 {user_answers.count(True)}문제를 맞추셨습니다.")
