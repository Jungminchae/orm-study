import re
import sys
import os


def check_format(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    pattern_question = re.compile(r"^\..+")
    pattern_empty_line = re.compile(r"^\s*$")
    pattern_answer = re.compile(r"^답\.\d$")
    pattern_separator = re.compile(r"^---$")

    errors = []

    i = 0
    while i < len(lines):
        if not pattern_question.match(lines[i]):
            errors.append(f"File: {file_path}, Line {i + 1}: Question must start with a dot.")

        i += 1
        if i >= len(lines) or not pattern_empty_line.match(lines[i]):
            errors.append(f"File: {file_path}, Line {i + 1}: There must be an empty line after the question.")

        i += 1
        answer_found = False
        while i < len(lines) and not pattern_separator.match(lines[i]):
            if pattern_answer.match(lines[i]):
                answer_found = True
            i += 1

        if not answer_found:
            errors.append(f"File: {file_path}, Line {i + 1}: Missing or incorrect answer format. Answer must start with '답.'")

        if i >= len(lines) or not pattern_separator.match(lines[i]):
            errors.append(f"File: {file_path}, Line {i + 1}: Must be followed by '---'")

        i += 1

    return errors


def find_and_check_files(root_dir: str) -> list[str]:
    all_errors = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file == "multiple_choice.txt":
                file_path = os.path.join(subdir, file)
                errors = check_format(file_path)
                all_errors.extend(errors)
    return all_errors


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_format.py <root_directory>")
        sys.exit(1)

    root_directory = sys.argv[1]
    all_errors = find_and_check_files(root_directory)

    if all_errors:
        print("Formatting errors found:")
        for error in all_errors:
            print(error)
        sys.exit(1)
    else:
        print("No formatting errors found.")
