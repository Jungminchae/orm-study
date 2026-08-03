import random
from typing import Annotated, List, Tuple

import typer
from rich import print
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from typer import Typer

from python_quiz.quiz.certification import generate_certification_image
from python_quiz.quiz.constants import (
    CHAPTER,
    CHAPTER_CHOICE,
    TYPE,
    TYPE_CHOICE,
)
from python_quiz.quiz.decorator import TimeTrace
from python_quiz.quiz.reader import get_chapter, parse_content

app = Typer()


def fetch_quiz(chapter_input: str, type_input: str) -> List[Tuple[str, str]]:
    try:
        quizzes = get_chapter(chapter_number=chapter_input, _type=type_input)
    except ValueError as msg:
        print(msg)
        raise typer.Exit(code=1)
    else:
        quizes_str, answers = parse_content(quizzes)
        quiz_answer_set = list(zip(quizes_str, answers))
        random.shuffle(quiz_answer_set)
        return quiz_answer_set


def fetch_exam() -> List[Tuple[str, str]]:
    all_quizzes = []
    for chapter_number in CHAPTER:
        for type_input in TYPE:
            quizzes = get_chapter(chapter_number, type_input, True)
            for q in quizzes:
                if q not in all_quizzes:
                    all_quizzes.append(q)

    quizes_str, answers = parse_content(all_quizzes)
    quiz_answer_set = list(zip(quizes_str, answers))
    random.shuffle(quiz_answer_set)
    return quiz_answer_set


def select_chapter() -> str:
    print(Panel(CHAPTER_CHOICE, title="챕터 선택", title_align="center", border_style="cyan"))
    chapter_input = Prompt.ask("[cyan bold]도전할 문제의 챕터를 선택해주세요[/cyan bold]")

    if chapter_input not in CHAPTER:
        print("[red bold]존재하지 않는 챕터입니다.[/red bold]")
        raise typer.Exit(code=1)

    return chapter_input


def select_quiz_type() -> str:
    print(Panel(TYPE_CHOICE, title="문제 유형 선택", title_align="center", border_style="magenta"))
    while True:
        type_input = Prompt.ask("[magenta bold]도전할 문제의 유형을 선택해주세요[/magenta bold]")
        if type_input not in TYPE:
            print("[red bold]존재하지 않는 유형입니다.[/red bold]")
        else:
            break
    return type_input


def select_quiz_num(max_num: int, min_num: int = 1) -> int:
    while True:
        msg = f"[bold yellow]문항 수를 선택해주세요. ({min_num} ~ {max_num}개)[/bold yellow]"
        quiz_num = Prompt.ask(msg)
        if not quiz_num:
            return max_num
        elif not quiz_num.isdigit():
            print("[red bold]숫자를 입력해주세요.[/red bold]")
        elif int(quiz_num) > max_num:
            print("[red bold]최대 문항 수를 넘을 수 없습니다.ㅠㅠ[/red bold]")
        elif int(quiz_num) < min_num:
            print(f"[red bold]최소 {min_num}개 이상 선택해야 합니다.[/red bold]")
        else:
            return int(quiz_num)


@TimeTrace
def solve_quiz(quiz_answer_set: List[Tuple[str, str]]) -> List[bool]:
    user_answers = []
    for i, (quiz, answer) in enumerate(quiz_answer_set, start=1):
        print(Panel(f"[white]{quiz}[/white]", title=f"[bold yellow]문제 {i}[/bold yellow]", title_align="center", border_style="yellow"))
        user_input = Prompt.ask("[bold cyan]✏️ 정답을 입력해주세요[/bold cyan]")
        while not user_input.strip():
            print("[red bold]⚠️ 정답을 입력하지 않았습니다. 찍기라도 하세요.[/red bold]")
            user_input = Prompt.ask("[bold cyan]✏️ 정답을 입력해주세요[/bold cyan]")

        is_correct = user_input.strip().lower() == answer.strip().lower()
        user_answers.append(is_correct)
        if is_correct:
            print("[bold green]✅ 정답입니다![/bold green]\n")
        else:
            print(f"[bold red]❌ 오답입니다. (정답: {answer})[/bold red]\n")

    return user_answers


def display_results(chapter_input: str, user_answers: List[bool]):
    correct_count = user_answers.count(True)
    total_count = len(user_answers)
    score_panel = Panel(
        f"[bold blue]총 {total_count}문제 중 {correct_count}문제를 맞추셨습니다.[/bold blue]\n\n"
        f"정답률: {correct_count/total_count*100:.1f}%",
        title=f"[bold green]챕터 {chapter_input} 퀴즈 결과[/bold green]",
        border_style="green",
    )
    print(score_panel)


def change_name(current_name: str) -> str:
    new_name = typer.prompt("새 이름을 입력해주세요. 현재 이름 =", default=current_name)
    if not new_name.strip():
        print(f"이름이 비어있습니다. [{current_name}]로 유지됩니다.")
        return current_name
    elif new_name == current_name:
        print(f"[{current_name}]로 유지됩니다.")
        return current_name
    print(f"이름이 [{new_name}]로 변경되었습니다.")
    return new_name


@app.command(help="파이썬 챕터별 퀴즈를 시작합니다.")
def start(
    time_check: Annotated[bool, typer.Option(help="퀴즈 타이머 추가")] = False,
):
    print("[green bold]🚀 파이썬 챕터별 퀴즈를 시작합니다.[/green bold]")
    chapter_input = select_chapter()
    type_input = select_quiz_type()
    quiz_answer_set = fetch_quiz(chapter_input, type_input)
    if not quiz_answer_set:
        print("[red bold]해당 조건에 맞는 문제가 없습니다.[/red bold]")
        raise typer.Exit(1)

    quiz_num = select_quiz_num(len(quiz_answer_set))
    print(f"\n[green bold]챕터 {chapter_input}: {CHAPTER[chapter_input]} 시작합니다![/green bold]\n")

    quiz_answer_set = quiz_answer_set[:quiz_num]
    user_answers, process_time = solve_quiz(quiz_answer_set)

    if time_check:
        print(f"[magenta bold]⏱️ 소요 시간: {process_time:.2f}초[/magenta bold]")

    display_results(chapter_input, user_answers)


@app.command(help="파이썬 종합 시험 모드를 시작합니다.")
def exam(
    time_check: Annotated[bool, typer.Option(help="시험 타이머 추가")] = False,
    name: Annotated[str, typer.Option(help="이름을 입력해주세요")] = "익명",
):
    print("[bold red]🔥 파이썬 종합 시험 모드에 진입했습니다.[/bold red]")
    name_change_mode = Prompt.ask(f"현재 이름은 [{name}]입니다. 이름을 변경하시겠습니까? (y/[N])")
    if name_change_mode.upper() == "Y":
        name = change_name(name)

    quiz_answer_set = fetch_exam()
    if not quiz_answer_set:
        print("[red bold]문제가 없습니다.[/red bold]")
        raise typer.Exit(1)

    quiz_num = select_quiz_num(len(quiz_answer_set), min_num=15)

    quiz_answer_set = quiz_answer_set[:quiz_num]
    user_answers, process_time = solve_quiz(quiz_answer_set)

    if time_check:
        print(f"[magenta bold]⏱️ 소요 시간: {process_time:.2f}초[/magenta bold]")

    print("[bold red]🏁 시험 종료[/bold red]")
    save_path = "./"
    generate_certification_image(name, user_answers, process_time, save_path)
    print(f"[bold blue]🎓 인증서가 다음 위치에 저장되었습니다: {save_path}[/bold blue]")


@app.command(name="stats", help="챕터별 퀴즈 통계를 보여줍니다.")
def stats():
    table = Table(title="📊 파이썬 퀴즈 통계", border_style="green")
    table.add_column("챕터 이름", style="cyan", no_wrap=True)
    table.add_column("객관식 (문제 수)", style="magenta")
    table.add_column("주관식 (문제 수)", style="yellow")
    table.add_column("총합", style="blue")

    total_mc = 0
    total_sub = 0

    for k, v in CHAPTER.items():
        quizzes = get_chapter(k, "3", True)
        mc_count = sum(1 for q in quizzes if q.get("type") == "multiple_choice")
        sub_count = sum(1 for q in quizzes if q.get("type") == "subjective")
        total_mc += mc_count
        total_sub += sub_count
        table.add_row(v, str(mc_count), str(sub_count), str(mc_count + sub_count))

    table.add_section()
    table.add_row("[bold]전체 합계[/bold]", f"[bold]{total_mc}[/bold]", f"[bold]{total_sub}[/bold]", f"[bold]{total_mc + total_sub}[/bold]")
    print(table)


@app.command(name="list", help="사용 가능한 퀴즈 챕터를 목록으로 출력합니다.")
def list_chapters():
    table = Table(title="📚 파이썬 퀴즈 챕터 목록", border_style="cyan")
    table.add_column("챕터 번호", style="cyan", no_wrap=True)
    table.add_column("챕터 이름", style="magenta")

    for k, v in CHAPTER.items():
        table.add_row(str(k), v)
    print(table)


if __name__ == "__main__":
    app()
