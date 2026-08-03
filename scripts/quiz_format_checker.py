import os
import json
import sys


def check_format(file_path: str) -> list[str]:
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"File: {file_path}: Invalid JSON - {str(e)}"]

    if not isinstance(data, list):
        return [f"File: {file_path}: Root should be a JSON array."]

    required_keys = {"id", "chapter", "type", "question", "answer"}

    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            errors.append(f"File: {file_path}, Item {idx}: Must be a JSON object.")
            continue

        missing_keys = required_keys - set(item.keys())
        if missing_keys:
            errors.append(f"File: {file_path}, Item {idx}: Missing required keys {missing_keys}.")

        # Additional format checks
        if "type" in item:
            if item["type"] not in ["multiple_choice", "subjective"]:
                errors.append(f"File: {file_path}, Item {idx}: 'type' must be 'multiple_choice' or 'subjective'.")

            if item["type"] == "multiple_choice" and "options" not in item:
                errors.append(f"File: {file_path}, Item {idx}: Missing 'options' for multiple_choice.")

    return errors


def find_and_check_files(root_dir: str) -> list[str]:
    all_errors = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file == "quiz.json":
                file_path = os.path.join(subdir, file)
                errors = check_format(file_path)
                all_errors.extend(errors)
    return all_errors


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quiz_format_checker.py <root_directory>")
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
