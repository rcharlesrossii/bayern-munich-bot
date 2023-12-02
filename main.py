import schedule
import time
import twitter
from datetime import datetime, timedelta
from LiveScore import LiveScore, Game
from typing import List


match_dates = {
                            20230818: 988969,
                            20230827: 989563,
                            20230902: 989543,
                            20230915: 989552,
                            20230920: 1071799,
                            20230923: 989580,
                            20230926: 970314,
                            20230930: 989578,
                            20231003: 1071800,
                            20231008: 989581,
                            20231021: 989608,
                            20231024: 1071802,
                            20231028: 989576,
                            20231101: 1097259,
                            20231104: 989579,
                            20231108: 1071809,
                            20231111: 989575,
                            20231124: 989516,
                            20231129: 1071807,
                            20231202: 989573,
                            20231209: 989499,
                            20231212: 1071804,
                            20231216: 989454,
                            20231219: 989423,
                            20240113: 989467,
                            20240120: 989497,
                            20240127: 989410,
                            20240203: 989421,
                            20240210: 989441,
                            20240217: 989501,
                            20240224: 989529,
                            20240302: 989452,
                            20240309: 989482,
                            20240316: 989539,
                            20240330: 989419,
                            20240406: 989358,
                            20240413: 989391,
                            20240420: 989377,
                            20240427: 989447,
                            20240504: 989376,
                            20240511: 989357,
                            20240518: 989347
                            }
team = "Bayern Munich"
todays_date = int(datetime.today().strftime("%Y%m%d"))
todays_id = match_dates[todays_date]

def tweet():
    if todays_date in match_dates.keys():
        match_dictionary = {
                            "date": todays_date,
                            "id": match_dates[todays_date],
                            "competition": 0,
                            "home team": 0,
                            "away team": 0,
                            "home score": 0,
                            "away score": 0,
                            "minute": 0,
                            "team": 0,
                            "player": 0,
                            "event": 0,
                            "status": 0
                            }
    
    livescore = LiveScore()
    match_info: List[Game] = livescore.getGames(todays_date, team)
    match_events = livescore.getGameInPlay(todays_id)

    events = match_events.events

    competition = match_info[0].competition
    home_team = match_info[0].home_team
    away_team = match_info[0].away_team

    tweet_log = []
    tweet_log_length = 0

    match_dictionary.update({"competition": competition})
    match_dictionary.update({"home team": home_team})
    match_dictionary.update({"away team": away_team})

    twitter.tweet(match_dictionary)

    while match_dictionary["status"] != "FT":
        if events is not None:
            for event in events:
                if event.team == match_dictionary["home team"]:
                    if event.event_type == "Goal" or event.event_type == "Own Goal" or event.event_type == "Penalty Goal":
                        match_dictionary["home score"] += 1

                if event.team == match_dictionary["away team"]:
                    if event.event_type == "Goal" or event.event_type == "Own Goal" or event.event_type == "Penalty Goal":
                        match_dictionary["away score"] += 1

                end_times = [45, 90, 105, 120]
                minute = event.minute
                if minute in end_times:
                    minute = str(minute) + "' + " + str(event.minute_extra)
                match_dictionary.update({"minute": minute})

                team = event.team
                match_dictionary.update({"team": team})
                
                player = event.player
                match_dictionary.update({"player": player})

                event_type = event.event_type
                match_dictionary.update({"event": event_type})

                if match_dictionary not in tweet_log:
                    tweet_log.append(match_dictionary)
                tweet_log_length += 1
                twitter.tweet(tweet_log[-1])
                time.sleep(1.5)

            status = match_events.status
            match_dictionary.update({"status": status})
            
            if status == "FT":
                match_dictionary.update({"minute": status})
                match_dictionary.update({"team": "ALL"})
                match_dictionary.update({"player": "ALL"})
                match_dictionary.update({"event": status})
                tweet_log.append(match_dictionary)
                twitter.tweet(tweet_log[-1])
                time.sleep(1.5)

schedule.every(1.5).minutes.until(timedelta(hours=3)).do(tweet)

while True:
    schedule.run_pending()
    time.sleep(1)
