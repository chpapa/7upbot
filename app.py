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

@app.event("app_mention")
def event_test(event, say):
    response = openai.ChatCompletion.create(
        engine="oursky-demo",
        messages = [ {"role":"system", "content": "You are an AI assistant."},
                     {"role": "user", "content": event["text"]}],
        temperature=0.5,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    say(response['choices'][0]['message']['content'])


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
