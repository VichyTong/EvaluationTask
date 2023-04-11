import json
import GPT

java_path = "../data/java_random_code.jsonl"
python_path = "../data/python_random_code.jsonl"

java_code = []
python_code = []


def read_code():
    with open(java_path, 'r') as f:
        for line in f:
            java_code.append(json.loads(line)["original_string"])
    with open(python_path, 'r') as f:
        for line in f:
            python_code.append(json.loads(line)["original_string"])


def main():
    read_code()

    test = java_code[0]
    req = GPT.send_request("Java", test, "What might be the input to this function? Give me some examples.")
    print(req)


main()
