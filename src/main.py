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
    GPT.get_information("Java", test)

    req = GPT.get_input("Java", test)
    print(req)
    ans = []
    for input_param in req["examples"]:
        ans.append(GPT.get_output("Java", test, input_param))
    print(ans)


main()
