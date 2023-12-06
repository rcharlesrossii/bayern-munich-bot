import tweepy
import twitter_keys


client = tweepy.Client(
                        twitter_keys.bearer_token,
                        twitter_keys.api_key,
                        twitter_keys.api_key_secret,
                        twitter_keys.access_token,
                        twitter_keys.access_token_secret,
                        wait_on_rate_limit=True
                        )

auth = tweepy.OAuthHandler(twitter_keys.api_key, twitter_keys.api_key_secret)
auth.set_access_token(twitter_keys.access_token, twitter_keys.access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

def tweet(match_updates):
    if match_updates["event"] == 0:
        tweet = "Today's {0} match between {1} and {2} is about to kick-off.\n\nWe should be set for an exciting match!".format(match_updates.get("competition"), match_updates.get("home team"), match_updates.get("away team"))
        client.create_tweet(text=tweet)
        print("Tweet sent!")
    
    if match_updates["event"] == "Goal":
        tweet = "GOAL!!!\n\n{0}'s {1} has scored a goal at the {2}' mark!\n\n{3} {4} - {5} {6}".format(match_updates.get("team"), match_updates.get("player"), match_updates.get("minute"), match_updates.get("home team"), match_updates.get("home score"), match_updates.get("away team"), match_updates.get("away score"))
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event"] == "Assist":
        tweet = "{0}'s {1} is credited for assisting the goal at the {2}' mark.".format(match_updates.get("team"), match_updates.get("player"), match_updates.get("minute"))
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event"] == "Own Goal":
        tweet = "Uh Oh...\n\n{0}'s {1} has scored an own goal at the {2}' mark!\n\n{3} {4} - {5} {6}".format(match_updates.get("team"), match_updates.get("player"), match_updates.get("minute"), match_updates.get("home team"), match_updates.get("home score"), match_updates.get("away team"), match_updates.get("away score"))
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event"] == "Penalty Goal":
        tweet = "WHAT INCREDIBLE PLACEMENT!\n\n{0}'s {1} kept his composure and scored his penalty kick at the {2}' mark!\n\n{3} {4} - {5} {6}".format(match_updates.get("team"), match_updates.get("player"), match_updates.get("minute"), match_updates.get("home team"), match_updates.get("home score"), match_updates.get("away team"), match_updates.get("away score"))
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event"] == "Penalty Miss":
        tweet = "Oh no!\n\n{0}'s {1} has failed to convert his penalty kick at the {2}' mark!".format(match_updates.get("team"), match_updates.get("player"), match_updates.get("minute"))
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event"] == "VAR":
        tweet = "What unfortunate luck for {0}!\n\nVAR has decided that {1}'s {0} did not score a goal at the {2}' mark!".format(match_updates.get("player"), match_updates.get("team"), match_updates.get("minute"))
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event"] == "Yellow Card":
        tweet = "{0}'s {1} has received a yellow card for his actions at the {2}' mark!".format(match_updates.get("team"), match_updates.get("player"), match_updates.get("minute"))
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event"] == "Second Yellow Card":
        tweet = "Goodbye {0}!\n\n{1}'s {0} has received his second yard at the {2}' mark and is forced off the pitch!\n\n{1} will be down a player for the rest of the match.".format(match_updates.get("player"), match_updates.get("team"), match_updates.get("minute"))
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event"] == "Red Card":
        tweet = "Things are getting serious now!\n\n{0}'s {1} has received a red card for his actions at the {2}' mark and is forced off the pitch!\n\n{0} will be down a player for the rest of the match.".format(match_updates.get("team"), match_updates.get("player"), match_updates.get("minute"))
        client.create_tweet(text=tweet)
        print("Tweet sent!")

    if match_updates["event"] == "FT":
        tweet = "The final whistle has blown, and that is the end of today's {0} match!\n\n{1} {2} - {3} {4}".format(match_updates.get("competition"), match_updates.get("home team"), match_updates.get("home score"), match_updates.get("away team"), match_updates.get("away score"))
        client.create_tweet(text=tweet)
        print("Tweet sent!")
