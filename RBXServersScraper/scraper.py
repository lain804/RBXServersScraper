import requests
from bs4 import BeautifulSoup
from .robot_challenge import Challenge
import json

DATA_SCRIPT_TAG_ID = "__NEXT_DATA__"
FETCH_LINK_ENDPOINT = "https://api.rbxservers.xyz/servers/v2/fetch-link"
HTML_PARSER = "lxml"

class Server:
    def __init__(self,server_id,place_id):
        self.server_id = server_id
        self.place_id = place_id
    
    def _get_challenge(self) -> Challenge:
        r = requests.get(f"https://rbxservers.xyz/servers/{self.server_id}")
        
        soup = BeautifulSoup(r.text,HTML_PARSER)
        data = soup.find("script", id=DATA_SCRIPT_TAG_ID).text
        
        data = json.loads(data)

        challenge_data = data["props"]["pageProps"]["data"]["robot_challenge"]

        return Challenge.from_base64(challenge_data)

    def get_link(self) -> str:
        challenge = self._get_challenge()
        payload = {
            'challenge_id': challenge.challenge_id,
            'challenge_solution': challenge.solve(),
            'ctx': 'WebPage',
        }
        r = requests.post(
            url=f"{FETCH_LINK_ENDPOINT}/{self.server_id}",
            json=payload
        )
        response_json = r.json()
        if response_json["success"]:
            return f"https://www.roblox.com/games/{self.place_id}?privateServerLinkCode={response_json["server_linkcode"]}"
        else:
            raise RuntimeError("failed to fetch server link")

class ServerScraper:
    def __init__(self,place_id) -> ServerScraper:
        self.place_id = place_id

    def get_servers(self) -> list[Server]:
        r = requests.get(f"https://rbxservers.xyz/games/{self.place_id}")

        soup = BeautifulSoup(r.text,HTML_PARSER)

        server_data_json = soup.find("script", id=DATA_SCRIPT_TAG_ID).text

        server_data = json.loads(server_data_json)

        servers = []

        data:dict = server_data["props"]["pageProps"]["data"]

        servers.extend(data.get("servers",[]))
        servers.extend(data.get("community_servers",[]))
        servers.extend(data.get("official_servers",[]))

        servers = [Server(server["id"], self.place_id) for server in servers]

        return servers
