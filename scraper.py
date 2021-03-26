from game_page import get_game_response
from player import PlayerInfo
from player_games_page import get_games_list_response, NUM_FETCH_GAMES



player_history_url = "/?begIndex=100&endIndex=350&"


def get_all_custom_games(player: PlayerInfo):
    games = []
    last_ind = 0
    while True:
        games_list_resp = get_games_list_resp(player, last_ind)
        for game in games_list_resp.games:
            if game.game_type == "CUSTOM_GAME":
                games.append(game)
        if games_list_resp.game_index_end - games_list_resp.game_index_begin < NUM_FETCH_GAMES:
            break
        last_ind = games_list_resp.game_index_end
    return games


def get_games_list_resp(player: PlayerInfo, begin_ind):
    return get_games_list_response(player.pid, begin_ind, player.token)


def get_game(game_id, player: PlayerInfo):
    return get_game_response(game_id, player.token)
