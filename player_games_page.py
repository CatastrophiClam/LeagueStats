import json
from request import get_acs_response


PLAYER_GAMES_PAGE_URL = "https://acs.leagueoflegends.com/v1/stats/player_history/NA1"
NUM_FETCH_GAMES = 20

class Game:

    def __init__(self, obj):
        self.game_id = obj["gameId"]
        self.game_duration = obj["gameDuration"]
        self.season_id = obj["seasonId"]
        self.game_version = obj["gameVersion"]
        self.game_type = obj["gameType"]

    def __str__(self):
        return f"{self.game_type} game {self.game_id} lasting {self.game_duration//60}m {self.game_duration%60}s"


class GamesListResponse:

    def __init__(self, obj):
        obj = obj["games"]
        self.game_index_begin = int(obj["gameIndexBegin"])
        self.game_index_end = int(obj["gameIndexEnd"])
        self.game_count = int(obj["gameCount"])
        self.games = [Game(game_obj) for game_obj in obj["games"]]

    def __str__(self):
        return f"Games list with games {self.game_index_begin} to {self.game_index_end} out of {self.game_count} total games"


def get_games_list_response(player_id, begin_ind, id_token):
    url = f"{PLAYER_GAMES_PAGE_URL}/{player_id}?begIndex={begin_ind}&endIndex={begin_ind+NUM_FETCH_GAMES}"
    resp = get_acs_response(url, id_token)
    obj = json.loads(resp.text)
    return GamesListResponse(obj)
