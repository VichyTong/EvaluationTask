import json
import os
import openai
import requests

import google_search

openai.api_key = os.environ['OPENAI_API_KEY']


def send_request(model, messages, temperature, top_p):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=3000,
        temperature=temperature,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["<<<"]
    )
    request = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
    }
    log = {
        'request': request,
        'response': response['choices'][0]['message']['content']
    }
    with open("../log/log.jsonl", 'a') as f:
        f.write(json.dumps(log) + '\n')

    return response['choices'][0]['message']['content']


def do_math(expression):
    try:
        return eval(expression)
    except Exception as e:
        print(e)
        return None


def get_input(language, code):
    messages = [
        {"role": "system",
         "content": "You are a helpful assistant. You will be given a code in " + language + ". Give some example input."},
        {"role": "user", "content": "int doMath(int a, int b){\nint c = a+b;\nreturn c;\n}"},
        {"role": "assistant",
         "content": "Let's think step by step.\nThere are two parameters in the function, a and b.\n a is an integer.\n b is an integer. According to the snippet, \n[ANS]: {\"param\": [{\"name\": \"a\", \"type\": \"int\"}, {\"name\": \"b\", \"type\": \"int\"}], \"examples\":[{\"a\": 1, \"b\": 2}, {\"a\": 2333, \"b\": -2000}, {\"a\": -3244, \"b\": 2345}]}"},
        {"role": "user", "content": code},
        {"role": "assistant", "content": "Let's think step by step."}
    ]
    res = send_request("gpt-3.5-turbo", messages, 0, 1)
    ans = res.split("[ANS]: ")[1]
    return json.loads(ans)


def get_output(language, code, input_param):
    messages = [
        {"role": "system",
         "content": "You are a helpful assistant. You will be given a code in " + language + ". Give the correct output for given input. Print output begin with [ANS]: "},
        {"role": "user", "content": "int doMath(int a, int b){\na ++;\nint c = (a+b) * a;\nreturn c;\n}"},
        {"role": "user",
         "content": 'INPUT: [{"a": 1, "b": 2}, {"a": 2333, "b": -2000}'},
        {"role": "assistant",
         "content": 'First, we increase a by 1.\nThen, we add a to b, and then multiply the result by a, we assign c by this result.\nFinally, we return c.\n1. {"a": 1, "b": 2}\na++ >>> 1 + 1 <<< 2\nSO a = 2\nc = (a + b) * a >>> (2 + 2) * 2 <<< 8\nSO c = 8\nreturn value is c\n>>> [ANS] = 8 <<<\n2. {"a": 2333, "b": -2000}\na++ >>> 2333 + 1 <<< 2334\nSO a = 2334\nc = (a + b) * a >>> (2334 + (-2000)) * 2334 <<< 779556\nSO c = 779556\nreturn value is c\n>>> [ANS] = 779556 <<<'},
        {"role": "user", "content": code},
        {"role": "user", "content": 'INPUT: ' + json.dumps(input_param)},
        {"role": "assistant", "content": "Let's think step by step."}
    ]
    flag = True
    ans = ""
    while flag:
        res = send_request("gpt-3.5-turbo", messages, 0, 1)
        info = res.split(">>> ")[-1]
        if info.startswith("[ANS]"):
            info = info.split("[ANS] = ")[-1]
            ans = info
            flag = False
        else:
            cal_res = do_math(info)
            if cal_res is not None:
                messages[-1]["content"] = messages[-1]["content"] + res + "<<<" + str(cal_res) + "\n"
            else:
                return None
    return ans


def get_information(language, code):
    messages = [
        {"role": "system",
         "content": "You are a helpful assistant. You will be given a code in " + language + ". What do you want to know about this code as you're required to generate a input and a output for it."},
        {"role": "user", "content": "private double findAttributeDouble(NetcdfDataset ds, String attname) {\nAttribute att = ds.findGlobalAttributeIgnoreCase(attname);\nif (att == null) return Double.NaN;\nreturn att.getNumericValue().doubleValue();\n}"},
        {"role": "assistant", "content": '["NetcdfDataset", "findGlobalAttributeIgnoreCase", "getNumericValue", "doubleValue"]'},
        {"role": "user", "content": code},
    ]
    res = send_request("gpt-3.5-turbo", messages, 0, 1)
    questions = json.loads(res)
    print(questions)
    messages = [
        {"role": "system", "content": "Do you know what is " + questions[0] + "? Give the original code."}
    ]
    res = send_request("gpt-3.5-turbo", messages, 0, 1)
    print(res)
