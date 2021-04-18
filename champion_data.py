import json
from Scrape.element import get_response

PATCH_NUMBER_URL = "https://ddragon.leagueoflegends.com/api/versions.json"

DATA_URL = "http://ddragon.leagueoflegends.com/cdn/{0}/data/en_US/champion.json"
champ_id_map = {}


def get_latest_patch():
    patch_data = json.loads(get_response(PATCH_NUMBER_URL).text)
    return patch_data[0]


def get_champ_id_map():
    if len(champ_id_map) > 0:
        return champ_id_map

    champ_data = json.loads(get_response(DATA_URL.format(get_latest_patch())).text)["data"]
    for champ, data in champ_data.items():
        champ_id_map[int(data["key"])] = champ
    return champ_id_map
