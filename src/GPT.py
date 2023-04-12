import json
import os
import openai

openai.api_key = os.environ['OPENAI_API_KEY']


def send_request(language, code, prompt):
    model = "gpt-3.5-turbo"
    temperature = 0
    messages = [
        {"role": "system", "content": "You are a helpful assistant. You will be given a code in " + language + ", then answer the question"},
        {"role": "user", "content": "Here is the code: " + code},
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": "Let's think step by step."}
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=3000,
        temperature=temperature,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["END"]
    )
    request = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }
    log = {
        'request': request,
        'response': response['choices'][0]['message']['content']
    }
    with open("../log/log.jsonl", 'a') as f:
        f.write(json.dumps(log) + '\n')

    return response['choices'][0]['message']['content']
