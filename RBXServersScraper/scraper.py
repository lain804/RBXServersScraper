import requests
from bs4 import BeautifulSoup
from .robot_challenge import Challenge
import json
import re

DATA_SCRIPT_TAG_ID = "__NEXT_DATA__"
FETCH_LINK_ENDPOINT = "https://api.rbxservers.xyz/servers/v2/fetch-link"
HTML_PARSER = "html.parser"

class Server:
    def __init__(self,server_id):
        self.server_id = server_id
    
    def _get_challenge(self) -> Challenge:
        r = requests.get(f"https://rbxservers.xyz/servers/{self.server_id}")
        r.raise_for_status()

        challenge_match = re.search(
            r'\\?"robot_challenge\\?"\s*:\s*\\?"([A-Za-z0-9_+/=-]+)\\?"',
            r.text,
        )
        if challenge_match is None:
            raise RuntimeError("failed to find robot challenge")
        challenge_data = challenge_match.group(1)

        return Challenge.from_base64(challenge_data)

    def get_link(self,place_id) -> str:
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
            return f"https://www.roblox.com/games/{place_id}?privateServerLinkCode={response_json["server_linkcode"]}"
        else:
            raise RuntimeError("failed to fetch server link")

class ServerScraper:
    def __init__(self,place_id) -> ServerScraper:
        self.place_id = place_id

    def get_servers(self) -> list[Server]:
        r = requests.get(f"https://rbxservers.xyz/games/{self.place_id}")
        r.raise_for_status()

        soup = BeautifulSoup(r.text,HTML_PARSER)

        servers = []

        for servers_holder in soup.find_all("div",class_="flex flex-col gap-2"):
            for anchor in servers_holder.find_all("a"):
                server_id = anchor["href"].split("/")[-1]
                server = Server(server_id)
                servers.append(server)

        return servers
