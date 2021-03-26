import json

from auth import player_max, player_mike
from player import PlayerInfo
from scraper import get_all_custom_games, get_game


max_games = get_all_custom_games(player_max)
mike_games = get_all_custom_games(player_mike)

game_ids_seen = set()
all_games = []
for game in max_games:
    if game.game_id in game_ids_seen:
        continue
    game_ids_seen.add(game.game_id)
    all_games.append((game, player_max))

for game in mike_games:
    if game.game_id in game_ids_seen:
        continue
    game_ids_seen.add(game.game_id)
    all_games.append((game, player_mike))


with open("out_data.tsv", "w") as out_f:
    headers = "Game ID\tGame Duration\tWinning Team"
    for i in range(10):
        headers += f"\tSummoner {i} Name\tTeam ID\tChampion\tPosition\tResult\tKills\tDeaths\tAssists"
    headers += "\n"
    out_f.write(headers)
    for game, player in all_games:
        game_info = None
        try:
            game_info = get_game(game.game_id, player)
        except json.decoder.JSONDecodeError:
            continue
        if len(game_info.participants) != 10:
            continue
        won_team = game_info.teams[0].team_id if game_info.teams[0].win else game_info.teams[1].team_id
        line = f"{game_info.game_id}\t{game_info.game_duration}\t{won_team}"

        sorted_participants = sorted(game_info.participants, key=lambda x: x.team_id)
        p_lines = []
        for participant in game_info.participants:
            p_lines.append(f"{participant.summoner_name}\t{participant.team_id}\t{participant.champion}\t{participant.position}\t" +
                           f"{'WIN' if participant.stats.win else 'LOSE'}\t{participant.stats.kills}\t{participant.stats.deaths}\t" +
                           f"{participant.stats.assists}")
        player_text = '\t'.join(p_lines)
        out_f.write(f"{line}\t{player_text}\n")

