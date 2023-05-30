# ChatGPTMail
This script is a simple tool for generating summaries of incoming emails in Polish using the OpenAI GPT-3 model (text-davinci-003). Upon receiving a new email, the script generates a summary and then sends it as a notification via the Pushover service.


## Imports
```
from os import getenv
from time import sleep

import openai
from dotenv import load_dotenv
from imap_tools import MailBox, A
from requests import post
```

- `os.getenv`: Used for reading environment variables.
- `time.sleep`: Used for introducing delay.
- `openai`: The OpenAI library, which allows interaction with the GPT-3 model.
- `dotenv.load_dotenv`: Used for loading environment variables from a .env file.
- `imap_tools.MailBox, A`: Used for interaction with an IMAP server.
- `requests.post`: Used for sending HTTP POST requests.


## Application Setup
```
load_dotenv()
client = MailBox(getenv('IMAP_HOST')).login(getenv('IMAP_LOGIN'), getenv('IMAP_PASSWORD'), 'INBOX')
openai.api_key = getenv('OPENAI_API')
```

The application setup starts by loading the environment variables from the `.env` file, then initializing the `MailBox` client and logging into the IMAP server. The OpenAI API key is also loaded as an environment variable.


## `chatgpt` Function
```
def chatgpt(text):
    ...
```

The `chatgpt` function uses the OpenAI GPT-3 model to generate summaries for the given text. It tries to perform the operation 6 times (adjustable via `retries` variable) and introduces a 20-second delay (set by `wait_time`) between attempts if the OpenAI API returns a rate limit error.


## `send_pushover` Function
```
def send_pushover(message, title):
    ...
```

The `send_pushover` function is used to send notifications via the Pushover service. In case the notification sending fails, the function returns error information.


## Main Loop
```
while 1:
    responses = client.idle.wait(timeout=60)
    ...
```

In the main loop of the program, the script waits for new email messages using the IMAP IDLE method. When a new message arrives, the script generates a summary for it and then sends it as a notification using the Pushover service. The loop runs indefinitely, checking the mailbox every minute (set by `timeout=60`).

All configuration variables (such as `IMAP_HOST`, `IMAP_LOGIN`, `IMAP_PASSWORD`, `OPENAI_API`, `PUSHOVER_TOKEN`, `PUSHOVER_USER`) should be set in the `.env` file.

Before running the code, ensure that all required libraries are installed and the appropriate environment variables are set.
