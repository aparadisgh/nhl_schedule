"""NHL API Utilities

This module contains utilities to get and transform data from the NHL API

Functions:
    nhl_api.get_games_by_dates: Retrieve game schedule by dates
    nhl_api.get_game_by_teams:  Retrieve game schedule for each team 

Dependencies:
    requests

"""

import json
import requests

def get_games_by_dates(start_date: str, end_date: str,) -> dict:
    """Retrieve game schedule by dates 

    Retrieves info of each game for a specific time period through the open NHL API

    Args:
        startDate (str): Start date of the desired time period in ISO format
        endDate (str): End date of the desired time period in ISO format (inclusive)

    Returns:
        dict: Returns the response from the NHL API as a dict

    Example:
        GET https://statsapi.web.nhl.com/api/v1/schedule?startDate=2022-10-12&endDate=2022-10-13

        {
            "copyright" : "NHL and the NHL Shield are registered trademarks of 
            the National Hockey League. NHL and NHL team marks are the property 
            of the NHL and its teams. © NHL 2022. All Rights Reserved.",
            "totalItems" : 16,
            "totalEvents" : 0,
            "totalGames" : 16,
            "totalMatches" : 0,
            "metaData" : {
                "timeStamp" : "20221015_113647"
            },
            "wait" : 10,
            "dates" : [ {
                "date" : "2022-10-12",
                "totalItems" : 6,
                "totalEvents" : 0,
                "totalGames" : 6,
                "totalMatches" : 0,
                "games" : [ {
                    "gamePk" : 2022020005,
                    "link" : "/api/v1/game/2022020005/feed/live",
                    "gameType" : "R",
                    "season" : "20222023",
                    "gameDate" : "2022-10-12T23:00:00Z",
                    "status" : {
                        "abstractGameState" : "Final",
                        "codedGameState" : "7",
                        "detailedState" : "Final",
                        "statusCode" : "7",
                        "startTimeTBD" : false
                    },
                    "teams" : {
                        "away" : {
                        "leagueRecord" : {
                            "wins" : 1,
                            "losses" : 0,
                            "ot" : 0,
                            "type" : "league"
                        },
                        "score" : 5,
                        "team" : {
                            "id" : 6,
                            "name" : "Boston Bruins",
                            "link" : "/api/v1/teams/6"
                        }
                        },
                        "home" : {
                        "leagueRecord" : {
                            "wins" : 0,
                            "losses" : 1,
                            "ot" : 0,
                            "type" : "league"
                        },
                        "score" : 2,
                        "team" : {
                            "id" : 15,
                            "name" : "Washington Capitals",
                            "link" : "/api/v1/teams/15"
                        }
                        }
                    },
                    "venue" : {
                        "id" : 5094,
                        "name" : "Capital One Arena",
                        "link" : "/api/v1/venues/5094"
                    },
                    "content" : {
                        "link" : "/api/v1/game/2022020005/content"
                    }
                }, 
                ...],
            },
            ...],
        }

    """
    r = requests.get(f'https://statsapi.web.nhl.com/api/v1/schedule?startDate={start_date}&endDate={end_date}')
    r_dict = json.loads(r.text)
    return r_dict['dates']


def get_game_by_teams(start_date: str, end_date: str, game_type: str ='R') -> dict:
    """Retrieve game schedule for each team 

    Retrieves minimal info of each game for a specific time period and game type

    Args:
        startDate (str): Start date of the desired time period in ISO format
        endDate (str): End date of the desired time period in ISO format (inclusive)
        game_type (str, optional): Game type defaulting to 'R' (Regular season), 
        'PR' (Pre-season), 'P' (Post-season), or 'all' (All types)

    Returns:
        dict: Dict of teams where values are lists of games (dict)

    """

    schedule = get_games_by_dates(start_date, end_date)

    games_per_team = {}
    for date in schedule:
        for game in date['games']:
            if game_type == 'all' or game_type == game['gameType']:
                home = game['teams']['home']['team']['id']
                away = game['teams']['away']['team']['id']

                if home in games_per_team:
                    games_per_team[home] = games_per_team[home]+[{
                        'date': date['date'],
                        'against': away,
                        'location': 'home',
                        'type':  game['gameType']
                    }]
                else:
                    games_per_team[home] = [{
                        'date': date['date'],
                        'against': away,
                        'location': 'home',
                        'type':  game['gameType']
                    }]

                if away in games_per_team:
                    games_per_team[away] = games_per_team[away]+[{
                        'date': date['date'],
                        'against': home,
                        'location': 'away',
                        'type':  game['gameType']
                    }]
                else:
                    games_per_team[away] = [{
                        'date': date['date'],
                        'against': home,
                        'location': 'away',
                        'type':  game['gameType']
                    }]

    return games_per_team

TEAM_ABBR = {
    "1": "NJD",
    "2": "NYI", 
    "3": "NYR", 
    "4": "PHI", 
    "5": "PIT", 
    "6": "BOS", 
    "7": "BUF", 
    "8": "MTL", 
    "9": "OTT", 
    "10": "TOR", 
    "12": "CAR", 
    "13": "FLA", 
    "14": "TBL",
    "15": "WSH",
    "16": "CHI", 
    "17": "DET",
    "18": "NSH", 
    "19": "STL", 
    "20": "CGY", 
    "21": "COL", 
    "22": "EDM", 
    "23": "VAN", 
    "24": "ANA", 
    "25": "DAL", 
    "26": "LAK", 
    "28": "SJS", 
    "29": "CBJ", 
    "30": "MIN", 
    "52": "WPG", 
    "53": "ARI", 
    "54": "VGK", 
    "55": "SEA"
}
