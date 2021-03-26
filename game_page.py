import json

from champion_data import get_champ_id_map
from request import get_acs_response


GAME_PAGE_URL = "https://acs.leagueoflegends.com/v1/stats/game/NA1"
champion_id_map = get_champ_id_map()

class Player:

    def __init__(self, participant_id, obj):
        self.participant_id = participant_id
        self.account_id = obj["accountId"]
        self.summoner_name = obj["summonerName"]
        self.summoner_id = obj["summonerId"]


class ParticipantStats:

    def __init__(self, obj):
        self.win = obj["win"]
        self.kills = obj["kills"]
        self.deaths = obj["deaths"]
        self.assists = obj["assists"]
        self.longest_time_spent_living = obj["longestTimeSpentLiving"]
        self.total_damage_dealt = obj["totalDamageDealt"]
        self.total_damage_dealt_to_champions = obj["totalDamageDealtToChampions"]
        self.total_damage_taken = obj["totalDamageTaken"]
        self.goldEarned = obj["goldEarned"]
        self.vision_score = obj["visionScore"]
        self.time_cc_others = obj["timeCCingOthers"]
        self.total_minions_killed = obj["totalMinionsKilled"]
        self.first_blood_kill = obj["firstBloodKill"]


class Participant:

    def __init__(self, player: Player, obj):
        self.participant_id = obj["participantId"]
        self.team_id = obj["teamId"]
        self.champion_id = obj["championId"]
        self.champion = champion_id_map[self.champion_id]
        self.stats = ParticipantStats(obj["stats"])
        self.role = obj["timeline"]["role"]
        self.lane = obj["timeline"]["lane"]
        self.summoner_name = player.summoner_name
        self.player = player

        self.position = "TOP"
        if self.role == "DUO_CARRY":
            self.position = "ADC"
        elif self.role == "DUO_SUPPORT":
            self.position = "SUPPORT"
        elif self.lane == "MIDDLE":
            self.position = "MID"
        elif self.lane == "JUNGLE":
            self.position = "JUNGLE"

    def __str__(self):
        return f"Participant {self.summoner_name} ({self.participant_id}) KDA {self.stats.kills}/{self.stats.deaths}/{self.stats.assists} " \
               f"team {self.team_id} playing {self.champion_id}"


class Team:

    def __init__(self, obj):
        self.team_id = obj["teamId"]
        self.win = obj["win"] == "Win"
        self.first_blood = obj["firstBlood"]
        self.first_tower = obj["firstTower"]
        self.first_inhibitor = obj["firstInhibitor"]
        self.first_baron = obj["firstBaron"]
        self.first_dragon = obj["firstDragon"]
        self.tower_kills = obj["towerKills"]
        self.bans = [ban_obj["championId"] for ban_obj in obj["bans"]]

    def __str__(self):
        return f"Team {self.team_id} {'Won' if self.win else 'Lost'}, banned {self.bans}"


class GameResponse:

    def __init__(self, obj):
        self.game_id = obj["gameId"]
        self.game_duration = int(obj["gameDuration"])
        self.game_mode = obj["gameMode"]
        self.game_type = obj["gameType"]
        self.teams = [Team(team_obj) for team_obj in obj["teams"]]
        self.players = {}
        for player_obj in obj["participantIdentities"]:
            self.players[player_obj["participantId"]] = Player(player_obj["participantId"], player_obj["player"])
        self.participants = [Participant(
            self.players[participant_obj["participantId"]], participant_obj
        ) for participant_obj in obj["participants"]]


def get_game_response(game_id, id_token):
    url = f"{GAME_PAGE_URL}/{game_id}"
    resp = get_acs_response(url, id_token)
    obj = None
    try:
        obj = json.loads(resp.text)
    except json.decoder.JSONDecodeError:
        print(resp.text)
        raise
    return GameResponse(obj)
