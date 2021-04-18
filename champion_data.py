import json
from Scrape.element import get_response

DATA_URL = "http://ddragon.leagueoflegends.com/cdn/11.7.1/data/en_US/champion.json"
champ_id_map = {}


def get_champ_id_map():
    if len(champ_id_map) > 0:
        return champ_id_map

    champ_data = json.loads(get_response(DATA_URL).text)["data"]
    for champ, data in champ_data.items():
        champ_id_map[int(data["key"])] = champ
    return champ_id_map
