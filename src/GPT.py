import os
import openai

openai.api_key = os.environ['OPENAI_API_KEY']


def send_request(language, code, prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You will be given a code in " + language + ", then answer the question"},
            {"role": "user", "content": "Here is the code: " + code},
            {"role": "user", "content": prompt}
        ],
        max_tokens=3000,
        temperature=0.1,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["END"]
    )
    return response['choices'][0]['message']['content']
