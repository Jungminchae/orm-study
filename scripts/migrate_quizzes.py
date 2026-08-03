import os
import json
import re


def parse_quiz_file(filepath, chapter, quiz_type, start_id):
    quizzes = []
    if not os.path.exists(filepath):
        return quizzes

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.split("---")
    current_id = start_id
    for block in blocks:
        block = block.strip()
        if not block:
            continue

        lines = block.split("\n")

        # question starts with .
        if not lines[0].startswith("."):
            continue

        question_lines = []
        options = []
        answer = ""

        # Remove the first '.' from the first line
        if lines and lines[0].startswith("."):
            lines[0] = lines[0][1:]

        for line in lines:
            line_stripped = line.strip()
            if line_stripped.startswith("답."):
                answer = line_stripped[2:].strip()
            elif quiz_type == "multiple_choice" and re.match(r"^[0-9]+\.\s+", line_stripped):
                # Clean prefix
                opt = re.sub(r"^[0-9]+\.\s+", "", line_stripped)
                options.append(opt)
            else:
                question_lines.append(line)

        # Clean up question text (remove extra blank lines at start/end)
        question_text = "\n".join(question_lines).strip()

        quiz = {
            "id": f"q{current_id}",
            "chapter": chapter,
            "type": quiz_type,
            "question": question_text,
            "options": options if quiz_type == "multiple_choice" else [],
            "answer": answer,
            "explanation": "",
        }

        quizzes.append(quiz)
        current_id += 1

    return quizzes


def main():
    base_dir = "orm_study/quiz/_python"

    # Optional: we can order chapters or just iterate
    for chapter in os.listdir(base_dir):
        chapter_dir = os.path.join(base_dir, chapter)
        if not os.path.isdir(chapter_dir) or chapter == "__pycache__":
            continue

        mc_file = os.path.join(chapter_dir, "multiple_choice.txt")
        sub_file = os.path.join(chapter_dir, "subjective.txt")

        mc_quizzes = parse_quiz_file(mc_file, chapter, "multiple_choice", 1)
        sub_quizzes = parse_quiz_file(sub_file, chapter, "subjective", len(mc_quizzes) + 1)

        all_quizzes = mc_quizzes + sub_quizzes

        out_file = os.path.join(chapter_dir, "quiz.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(all_quizzes, f, ensure_ascii=False, indent=2)

        print(f"[{chapter}] Converted: {len(mc_quizzes)} MC, {len(sub_quizzes)} Sub -> {out_file}")


if __name__ == "__main__":
    main()
