import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import ssl
from flask import Flask
from slackeventsapi import SlackEventAdapter
ssl._create_default_https_context = ssl._create_unverified_context
env_path = Path(".") / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], "/slack/events", app)
@app.route("/")
def hello():
  return "Hello there!"
# Create an event listener for "reaction_added" events and print the emoji name
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
  emoji = event_data["event"]["reaction"]
  print(emoji)
  
@slack_events_adapter.on("message")
def message_added(event_data):
  message = event_data["event"]['text']
  print(message)
  
  
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
# print(os.environ['SLACK_TOKEN'])

client.chat_postMessage(channel="#slack-bot-test", text="Hello World!")

if __name__ == "__main__":
    app.run(debug=True)