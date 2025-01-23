import match_dates
import time
import twitter
import traceback
from datetime import datetime
from LiveScore import LiveScore, Game
from typing import List


match_dates = match_dates.match_dates

def tweet():
    team = "Bayern Munich"
    todays_date = int(datetime.today().strftime("%Y%m%d"))
    todays_id = match_dates[todays_date][0]

    if todays_date in match_dates.keys():
        match_dictionary = {
                            "date": todays_date,
                            "id": match_dates[todays_date][0],
                            "start time": match_dates[todays_date][1],
                            "competition": 0,
                            "home team": 0,
                            "home team code": match_dates[todays_date][2],
                            "home score": 0,
                            "away team": 0,
                            "away team code": match_dates[todays_date][3],
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
        match_dictionary.update({"competition": competition})

        home_team = match_info[0].home_team
        match_dictionary.update({"home team": home_team})

        away_team = match_info[0].away_team
        match_dictionary.update({"away team": away_team})

        twitter.tweet(match_dictionary)
        print(match_dictionary)

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
            if match_events:
                print(match_events)
            if match_events and match_events.events != None:
                events = match_events.events
                if events:
                    for event in events:
                        if event.team == match_dictionary["home team"]:
                            if event.event_type == "Goal" or event.event_type == "Own Goal" or event.event_type == "Penalty Goal":
                                match_dictionary.update({"home score": event.home_score_updated})
                            if event.event_type == "VAR":
                                match_dictionary.update({"home score": event.home_score_updated})

                        if event.team == match_dictionary["away team"]:
                            if event.event_type == "Goal" or event.event_type == "Own Goal" or event.event_type == "Penalty Goal":
                                match_dictionary.update({"away score": event.away_score_updated})
                            if event.event_type == "VAR":
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
                                try:
                                    event_log.append(event_dictionary)
                                    match_dictionary["event count"] += 1
                                    twitter.tweet(match_dictionary)
                                    print(match_dictionary)
                                except Exception:
                                    print(traceback.print_exc())

                        status = match_events.status
                        match_dictionary.update({"status": status})

                        # Check if the status is "HT" and if "HT" is not already in event_log
                        # LiveScore gets buggy and sometimes shows "HT" multiple times with different scores
                        if status == "HT" and not any(event['event type'] == "HT" for event in event_log):
                            try:
                                match_dictionary.update({"minute": status})
                                match_dictionary.update({"team": "ALL"})
                                match_dictionary.update({"player": "ALL"})
                                match_dictionary.update({"event type": status})
                                match_dictionary.update({"status": status})
                                match_dictionary.update({"minute": status})
                                event_log.append(event_dictionary)
                                twitter.tweet(match_dictionary)
                                print(match_dictionary)
                            except Exception:
                                print(traceback.print_exc())

                        # Check if the status is "HT" and is already in event_log
                        if status == "HT" and any(event['event type'] == "HT" for event in event_log):
                            pass

                        if status == "FT":
                            try:
                                match_dictionary.update({"home score": match_events.home_score})
                                match_dictionary.update({"away score": match_events.away_score})
                                match_dictionary.update({"minute": status})
                                match_dictionary.update({"team": "ALL"})
                                match_dictionary.update({"player": "ALL"})
                                match_dictionary.update({"event type": status})
                                match_dictionary.update({"status": status})
                                twitter.tweet(match_dictionary)
                                print(match_dictionary)
                                return
                            except Exception:
                                print(traceback.print_exc())
            time.sleep(120)

tweet = tweet()
