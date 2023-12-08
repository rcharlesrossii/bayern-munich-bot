import time
import twitter
from datetime import datetime
from LiveScore import LiveScore, Game
from typing import List


def tweet():
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
                    20231105: 1064851,
                    20231108: 1071809,
                    20231111: 989575,
                    20231124: 989516,
                    20231129: 1071807,
                    20231209: 989499,
                    20231212: 1071804,
                    20231216: 989454,
                    20231219: 989423,
                    20240113: 989467,
                    20240120: 989497,
                    20240124: 989573,
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
                            "event type": 0,
                            "event count": 0,
                            "event id": 0,
                            "status": 0
                            }
    
        livescore = LiveScore()
        match_info: List[Game] = livescore.getGames(todays_date, team)

        competition = match_info[0].competition
        home_team = match_info[0].home_team
        away_team = match_info[0].away_team

        match_dictionary.update({"competition": competition})
        match_dictionary.update({"home team": home_team})
        match_dictionary.update({"away team": away_team})

        twitter.tweet(match_dictionary)

        event_log = []

        event_dictionary = {
                            "event type": match_dictionary["event type"],
                            "event_id": match_dictionary["event id"],
                            "minute": match_dictionary["minute"]
                            }
        
        event_log.append(event_dictionary)
        match_dictionary["event count"] += 1

        while match_dictionary["status"] != "FT":
            match_events = livescore.getGameInPlay(todays_id)
            if match_events and match_events.events != None:
                events = match_events.events
                if events:
                    for event in events:
                        if event.team == match_dictionary["home team"]:
                            if event.event_type == "Goal" or event.event_type == "Own Goal" or event.event_type == "Penalty Goal":
                                match_dictionary.update({"home score": event.home_score_updated})

                        if event.team == match_dictionary["away team"]:
                            if event.event_type == "Goal" or event.event_type == "Own Goal" or event.event_type == "Penalty Goal":
                                match_dictionary.update({"away score": event.away_score_updated})

                        end_times = [45, 90, 105, 120]
                        minute = event.minute
                        if minute in end_times and event.minute_extra != None:
                            minute = str(minute) + "' + " + str(event.minute_extra)
                        match_dictionary.update({"minute": minute})

                        team = event.team
                        match_dictionary.update({"team": team})
                        
                        player = event.player
                        match_dictionary.update({"player": player})

                        event_type = event.event_type
                        match_dictionary.update({"event type": event_type})
                        
                        event_id = event.event_id
                        match_dictionary.update({"event id": event_id})

                        event_dictionary = {
                                            "event type": match_dictionary["event type"],
                                            "event_id": match_dictionary["event id"],
                                            "minute": match_dictionary["minute"]
                                            }

                        if event_dictionary not in event_log:
                            if player != None:
                                event_log.append(event_dictionary)
                                match_dictionary["event count"] += 1
                                twitter.tweet(match_dictionary)

                        status = match_events.status

                        if status == "FT" and match_dictionary["event count"] == (len(events) + 1):
                            match_dictionary.update({"home score": event.home_score_updated})
                            match_dictionary.update({"away score": event.away_score_updated})
                            match_dictionary.update({"minute": status})
                            match_dictionary.update({"team": "ALL"})
                            match_dictionary.update({"player": "ALL"})
                            match_dictionary.update({"event type": status})
                            match_dictionary.update({"status": status})
                            twitter.tweet(match_dictionary)
                            return
                        
            time.sleep(60)

tweet = tweet()
