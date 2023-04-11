import json
import random

java_file_path = "../data/java/final/jsonl/test/java_test_0.jsonl"
python_file_path = "../data/python/final/jsonl/test/python_test_0.jsonl"


def read_random_lines_from_jsonl_file(file_path):
    lines = []
    with open(file_path, 'r') as f:
        for line in f:
            lines.append(json.loads(line))
    return random.sample(lines, 20)


if __name__ == "__main__":
    java_code = read_random_lines_from_jsonl_file(java_file_path)
    python_code = read_random_lines_from_jsonl_file(python_file_path)
    print(java_code)
    with open("java_random_code.jsonl", 'w') as f:
        for code in java_code:
            f.write(json.dumps(code) + '\n')
    with open("python_random_code.jsonl", 'w') as f:
        for code in python_code:
            f.write(json.dumps(code) + '\n')
