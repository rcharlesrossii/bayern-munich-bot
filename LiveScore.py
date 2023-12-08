import httpx
from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass
class Game:
    competition: str
    country: str
    game_id: int
    home_team: str
    away_team: str
    start_time: int

@dataclass
class Event:
    event_id: int
    minute: int
    minute_extra: int
    player: str
    team: str
    event_type: str
    home_score_updated: int
    away_score_updated: int

@dataclass
class GameInPlay:
    game_id: int
    status: int
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    events: List[Event]

class LiveScore:
    date_today = None

    def convertType(self, type):
        match type:
            case 36:
                return 'Goal'
            case 37:
                return 'Penalty Goal'
            case 38:
                return 'Penalty Miss'
            case 39:
                return 'Own Goal'
            case 40:
                return 'Penalty Shootout Miss'
            case 41:
                return 'Penalty Shootout Goal'
            case 43:
                return 'Yellow Card'
            case 44:
                return 'Second Yellow Card'
            case 45:
                return 'Red Card'
            case 62:
                return 'VAR'
            case 63:
                return 'Assist'

    def __init__(self):
        global date_today

        date_today = date.today().strftime('%Y%m%d')

    def getGames(self, date=None, team=None):
        if date == None:
            date = date_today
        
        response = httpx.get(f'https://prod-public-api.livescore.com/v1/api/app/date/soccer/{date}/1?countryCode=GB&locale=en')

        response_json = response.json()

        games = []

        for game in response_json['Stages']:
            competition = game['CompN'] if 'CompN' in game else game['Snm']
            country = game['Cnm']

            for event in game['Events']:
                game_id = event['Eid']
                home_team = event['T1'][0]['Nm']
                away_team = event['T2'][0]['Nm']
                start_time = event['Esd']

                games.append(Game(
                    competition=competition,
                    country=country,
                    game_id=game_id,
                    home_team=home_team,
                    away_team=away_team,
                    start_time=start_time
                ))

        if team == None:
            if games:
                return games
            else:
                return None
        else:
            filtered_games = []

            for game in games:
                if game.home_team == team or game.away_team == team:
                    filtered_games.append(game)

            if filtered_games:
                return filtered_games
            else:
                return None

    def getGameInPlay(self, id):
        response = httpx.get(f'https://prod-public-api.livescore.com/v1/api/app/scoreboard/soccer/{id}?locale=en')

        response_json = response.json()

        game_id = response_json['Eid']
        status = response_json['Eps']
        home_team = response_json['T1'][0]['Nm']
        away_team = response_json['T2'][0]['Nm']
        
        if status == 'NS':
            return None
        
        home_score = response_json['Tr1']
        away_score = response_json['Tr2']

        events_response = httpx.get(f'https://prod-public-api.livescore.com/v1/api/app/incidents/soccer/{id}?locale=en')

        events_response_json = events_response.json()

        if 'Incs' in events_response_json:
            if len(events_response_json['Incs']) > 0:
                events = []

                for root_event in events_response_json['Incs']:
                    for event in events_response_json['Incs'][root_event]:
                        if 'Incs' in event:
                            for sub_event in event['Incs']:
                                event_id = sub_event['ID']
                                minute = sub_event['Min'] if 'Min' in sub_event else None
                                minute_extra = sub_event['MinEx'] if 'MinEx' in sub_event else None
                                player = sub_event['Pn'] if 'Pn' in sub_event else None
                                team = home_team if sub_event['Nm'] == 1 else away_team
                                event_type = self.convertType(sub_event['IT'])
                                home_score_updated = sub_event['Sc'][0] if 'Sc' in sub_event else None
                                away_score_updated = sub_event['Sc'][1] if 'Sc' in sub_event else None

                                events.append(Event(
                                    event_id=event_id,
                                    minute=minute,
                                    minute_extra=minute_extra,
                                    player=player,
                                    team=team,
                                    event_type=event_type,
                                    home_score_updated=home_score_updated,
                                    away_score_updated=away_score_updated
                                ))
                        else:
                            event_id = event['ID']
                            minute = event['Min'] if 'Min' in event else None
                            minute_extra = event['MinEx'] if 'MinEx' in event else None
                            player = event['Pn'] if 'Pn' in event else None
                            team = home_team if event['Nm'] == 1 else away_team
                            event_type = self.convertType(event['IT'])
                            home_score_updated = event['Sc'][0] if 'Sc' in event else None
                            away_score_updated = event['Sc'][1] if 'Sc' in event else None

                            events.append(Event(
                                event_id=event_id,
                                minute=minute,
                                minute_extra=minute_extra,
                                player=player,
                                team=team,
                                event_type=event_type,
                                home_score_updated=home_score_updated,
                                away_score_updated=away_score_updated
                            ))
            else:
                events = None
        else:
            events = None

        return GameInPlay(
            game_id=game_id,
            status=status,
            home_team=home_team,
            away_team=away_team,
            home_score=home_score,
            away_score=away_score,
            events=events
        )
