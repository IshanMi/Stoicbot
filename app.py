import os
from dotenv import load_dotenv, find_dotenv
from slack_bolt import App
from datetime import date

load_dotenv(find_dotenv())

app = App(
    token=os.getenv("BOT_USER_OAUTH"),
    signing_secret=os.getenv("SIGNING_SECRET"),
    name="Stoicbot"
)


def today_date():
    return date.today().strftime("%B %d")


@app.event("app_home_opened")
def post_message():
    return "The obstacle is the way"
