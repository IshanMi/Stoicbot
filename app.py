import os
from dotenv import load_dotenv, find_dotenv
from slack_bolt import App
from datetime import date
from json import load

load_dotenv(find_dotenv())

app = App(
    token=os.getenv("BOT_USER_OAUTH"),
    signing_secret=os.getenv("SIGNING_SECRET"),
    name="Stoicbot"
)

CHANNEL = os.getenv("CHANNEL")

with open("pdf_parsing/Stoic_log.json") as f:
    entries = load(f)


def get_date():
    return date.today().strftime("%B %d")


def get_message():
    return entries[get_date()]['title']


@app.message("today")
def post_message(say):
    say(f'{get_date()}: {get_message()}')


@app.event("channel_joined")
def welcome_new_user(say):
    say(text="Welcome to the Daily Stoic Challenge! Here's where you'll be encouraged to embrace some of the ideas of "
             "the philosophy of stoicism, and apply them to make your life better. I'm Stoicbot, I'll be posting a new "
             "thought from the Daily Stoic every day."
             ""
             "If you notice any bugs, please feel free to reach out to @Ishan or @pybob",
        channel=CHANNEL)
