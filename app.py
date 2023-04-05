import os
import openai
# Use the package we installed
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
)

openai.api_type = "azure"
openai.api_base = os.environ["OPENAI_API_BASE"]
openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_version = "2023-03-15-preview"

threads = {} 

def handle_prompt(ts, text, say):
    if ts not in threads:
        threads[ts] = [ {"role":"system", "content": "You are an AI assistant."} ]

    threads[ts].append({"role":"user", "content": text})

    print(threads[ts])

    response = openai.ChatCompletion.create(
        engine="oursky-demo",
        messages = threads[ts],
        temperature=0.5,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    response = response['choices'][0]['message']['content']
    threads[ts].append({"role":"assistant", "content":response})

    say(response, thread_ts=ts)

@app.event("app_mention")
def event_prompt(event, say):
    ts = event["ts"]

    handle_prompt(ts, event["text"], say)


@app.event("message")
def event_reply(event, say):
    ts = event.get("thread_ts")

    if ts is None:
        return

    if ts in threads:
        handle_prompt(ts, event["text"], say)


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
