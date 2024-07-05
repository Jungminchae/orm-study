from typer import Typer
from quiz.command import app as quiz_app


app = Typer()
app.add_typer(quiz_app, name="quiz")


def main():
    app()


if __name__ == "__main__":
    main()
