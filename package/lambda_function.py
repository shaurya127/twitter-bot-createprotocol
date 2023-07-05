import tweepy
from dotenv import load_dotenv
import os
from requests_oauthlib import OAuth1Session
import csv
from telegram import Bot
import asyncio
from pathlib import Path
# Load environment variables
load_dotenv()

ROOT = Path(__file__).resolve().parents[0]

# Twitter API credentials
bearer_token = os.getenv("BEARER_TOKEN")
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")


bot_token = '6062435791:AAHhm3SSh-u9ygq-YWwYg14WBd2lnrc02Fg'
group_ids = ['-845538975', '-844376939']  # Add more group IDs here

# Initialize the Telegram bot
bot = Bot(token=bot_token)


def api():
    return tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)


def createTweet(api: tweepy.Client, tweet_text: str, tweet_link: str, access_token: str, access_token_secret: str) -> str:
    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )
    payload = {"text": f"{tweet_text}\n\n{tweet_link}"}

    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

    tweet_id = response.json()["data"]["id"]
    return tweet_id
    
async def lambda_handler(event,context):
    api_instance = api()
    reply_csv_file = ROOT / "reply.csv"
    tweet_text = ""
    tweet_link = ""
    row_index = -1


    with open(reply_csv_file, newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)
        for i, row in enumerate(rows):
            if len(row) >= 3 and int(row[2]) == 0:
                tweet_link = row[1]
                tweet_text = row[0]
                row_index = i
                break

    if tweet_text and tweet_link:
        tweet_id = createTweet(api_instance, tweet_text, tweet_link, access_token, access_token_secret)
        print("Tweet posted successfully. Tweet ID:", tweet_id)

        for group_id in group_ids:

            await bot.send_message(chat_id=group_id, text=tweet_link)  # Send the tweet link first
            await asyncio.sleep(1)  # Add a delay between messages
            await bot.send_message(chat_id=group_id, text=tweet_text)  # Send the reply text

        if row_index >= 0:
            rows[row_index][2] = "1"
            with open(reply_csv_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            print("Flag updated to 1 in reply.csv for row index:", row_index)
    else:
        print("No unused text found in reply.csv")



    

