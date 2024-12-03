import os
import tweepy
from datetime import datetime


ACCESS_TOKEN = os.environ["access_token"]
ACCESS_TOKEN_SECRET = os.environ["access_token_secret"]
API_KEY = os.environ["api_key"]
API_KEY_SECRET = os.environ["api_key_secret"]
BEARER_TOKEN = os.environ["bearer_token"]
CLIENT_SECRET = os.environ["client_secret"]
CLIENT_TOKEN = os.environ["client_token"]

client = tweepy.Client(
                        BEARER_TOKEN,
                        API_KEY,
                        API_KEY_SECRET,
                        ACCESS_TOKEN,
                        ACCESS_TOKEN_SECRET,
                        wait_on_rate_limit=True
                        )

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)

today = datetime.date.today()
date = today.strftime("%m/%d/%Y")

def tweet(match_updates):
    if match_updates["event type"] == 0:
        tweet = "Today's {0} match between {1} and {2} is about to kick-off.\n\nWe should be set for an exciting match!\n\n#{3}vs{4} {5}".format(match_updates.get("competition"), match_updates.get("home team"), match_updates.get("away team"), match_updates.get("home team code"), match_updates.get("away team code"), date)
        client.create_tweet(text=tweet)
        print("Tweet sent!")
    
    if match_updates["event type"] == "Goal":
        tweet = "GOAL!!!\n\n{0}'s {1} has scored a goal at the {2}' mark!\n\n{3} {4} - {5} {6}\n\n#{7}vs{8} {9}".format(match_updates.get("team"), match_updates.get("player"), match_updates.get("minute"), match_updates.get("home team"), match_updates.get("home score"), match_updates.get("away team"), match_updates.get("away score"), match_updates.get("home team code"), match_updates.get("away team code"), date)
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event type"] == "Assist":
        tweet = "{0}'s {1} is credited for assisting the goal at the {2}' mark.\n\n#{3}vs{4} {5}".format(match_updates.get("team"), match_updates.get("player"), match_updates.get("minute"), match_updates.get("home team code"), match_updates.get("away team code"), date)
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event type"] == "Own Goal":
        if match_updates["team"] == match_updates["home team"]:
            tweet = "Uh Oh...\n\n{0}'s {1} has scored an own goal at the {2}' mark!\n\n{3} {4} - {0} {5}\n\n#{6}vs{7} {8}".format(match_updates.get("away team"), match_updates.get("player"), match_updates.get("minute"), match_updates.get("home team"), match_updates.get("home score"), match_updates.get("away score"), match_updates.get("home team code"), match_updates.get("away team code"), date)
            client.create_tweet(text=tweet)
            print("Tweet sent!")
        if match_updates["team"] == match_updates["away team"]:
            tweet = "Uh Oh...\n\n{0}'s {1} has scored an own goal at the {2}' mark!\n\n{0} {3} - {4} {5}\n\n#{6}vs{7} {8}".format(match_updates.get("home team"), match_updates.get("player"), match_updates.get("minute"), match_updates.get("home score"), match_updates.get("away team"), match_updates.get("away score"), match_updates.get("home team code"), match_updates.get("away team code"), date)
            client.create_tweet(text=tweet)
            print("Tweet sent!")

    if match_updates["event type"] == "Penalty Goal":
        tweet = "WHAT INCREDIBLE PLACEMENT!\n\n{0}'s {1} kept his composure and scored his penalty kick at the {2}' mark!\n\n{3} {4} - {5} {6}\n\n#{7}vs{8} {9}".format(match_updates.get("team"), match_updates.get("player"), match_updates.get("minute"), match_updates.get("home team"), match_updates.get("home score"), match_updates.get("away team"), match_updates.get("away score"), match_updates.get("home team code"), match_updates.get("away team code"), date)
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event type"] == "Penalty Miss":
        tweet = "Oh no!\n\n{0}'s {1} has failed to convert his penalty kick at the {2}' mark!\n\n#{3}vs{4} {5}".format(match_updates.get("team"), match_updates.get("player"), match_updates.get("minute"), match_updates.get("home team code"), match_updates.get("away team code"), date)
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event type"] == "VAR":
        tweet = "What unfortunate luck for {0}!\n\nVAR has decided that {0}'s {1} goal at the {2}' mark will not count!\n\n{3} {4} - {5} {6}\n\n#{7}vs{8} {9}".format(match_updates.get("team"), match_updates.get("player"), match_updates.get("minute"), match_updates.get("home team"), match_updates.get("home score"), match_updates.get("away team"), match_updates.get("away score"), match_updates.get("home team code"), match_updates.get("away team code"), date)
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event type"] == "Yellow Card":
        tweet = "{0}'s {1} has received a yellow card for his actions at the {2}' mark!\n\n#{3}vs{4} {5}".format(match_updates.get("team"), match_updates.get("player"), match_updates.get("minute"), match_updates.get("home team code"), match_updates.get("away team code"), date)
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event type"] == "Second Yellow Card":
        tweet = "Goodbye {0}!\n\n{1}'s {0} has received his second yard at the {2}' mark and is forced off the pitch!\n\n{1} will be down a player for the rest of the match.\n\n#{3}vs{4} {5}".format(match_updates.get("player"), match_updates.get("team"), match_updates.get("minute"), match_updates.get("home team code"), match_updates.get("away team code"), date)
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event type"] == "Red Card":
        tweet = "Things are getting serious now!\n\n{0}'s {1} has received a red card for his actions at the {2}' mark and is forced off the pitch!\n\n{0} will be down a player for the rest of the match.\n\n#{3}vs{4} {5}".format(match_updates.get("team"), match_updates.get("player"), match_updates.get("minute"), match_updates.get("home team code"), match_updates.get("away team code"), date)
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event type"] == "HT":
        tweet = "The first half of today's {0} match has finished, we will tune back in 15 minutes for the remainder of the match!\n\n{1} {2} - {3} {4}\n\n#{5}vs{6} {7}".format(match_updates.get("competition"), match_updates.get("home team"), match_updates.get("home score"), match_updates.get("away team"), match_updates.get("away score"), match_updates.get("home team code"), match_updates.get("away team code"), date)
        client.create_tweet(text=tweet)
        print("Tweet sent!")
    
    if match_updates["event type"] == "FT":
        tweet = "The final whistle has blown, and that is the end of today's {0} match!\n\n{1} {2} - {3} {4}\n\n#{5}vs{6} {7}".format(match_updates.get("competition"), match_updates.get("home team"), match_updates.get("home score"), match_updates.get("away team"), match_updates.get("away score"), match_updates.get("home team code"), match_updates.get("away team code"), date)
        client.create_tweet(text=tweet)
        print("Tweet sent!")
