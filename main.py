from os import getenv
from time import sleep

import openai
from dotenv import load_dotenv
from imap_tools import MailBox, A
from requests import post


# Set up the application
load_dotenv()
client = MailBox(getenv('IMAP_HOST')).login(getenv('IMAP_LOGIN'), getenv('IMAP_PASSWORD'), 'INBOX')
openai.api_key = getenv('OPENAI_API')


def chatgpt(text):
    retries = 6
    wait_time = 20

    for i in range(retries):
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=text,
                temperature=0,
                max_tokens=200,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response.choices[0].text.strip()
        except openai.error.RateLimitError:
            print(f"Rate limit exceeded, retrying after {wait_time} seconds.")
            sleep(wait_time)
    print("Failed to summarize the text after multiple retries.")
    return None


def send_pushover(message, title):
    url = "https://api.pushover.net/1/messages.json"
    data_push = {
        "token": getenv('PUSHOVER_TOKEN'),
        "user": getenv('PUSHOVER_USER'),
        "message": message,
        "title": title
    }
    response = post(url, data=data_push)
    if response.status_code != 200:
        print(f"Failed to send Pushover notification: {response.text}")


while 1:
    responses = client.idle.wait(timeout=60)
    if responses:
        for msg in client.fetch(A(seen=False)):
            res = chatgpt(f'Summarize in one sentence in Polish email from \"{msg.from_}\" with subject \"{msg.subject}\".')
            send_pushover(res, msg.from_)
