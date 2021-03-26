from Scrape.element import get_response


REQUIRED_HEADER = {
    'authority': 'acs.leagueoflegends.com',
    'method': 'GET',
    'path': '/v1/stats/player_history/NA1/214576762?begIndex=100&endIndex=350&',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
}


def get_acs_response(url, id_token):
    header = REQUIRED_HEADER.copy()
    header["cookie"] = f"id_token={id_token}"
    return get_response(url, header)
