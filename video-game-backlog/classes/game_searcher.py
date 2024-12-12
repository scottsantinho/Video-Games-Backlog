# -*- coding: utf-8 -*-
# This class will handle searching for games using the RAWG.io API.
# API docs: https://rawg.io/

import requests

class GameSearcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.rawg.io/api/games"

    def search_games(self, query, platform_id=None, page_size=30):
        # Perform a search using RAWG API with optional platform filtering.
        params = {
            "search": query,
            "key": self.api_key,
            "page_size": page_size
        }
        if platform_id is not None:
            params["platforms"] = platform_id

        response = requests.get(self.base_url, params=params)
        data = response.json()
        results = data.get("results", [])
        return results

    def get_game_data_row(self, game_info):
        # Extract relevant info: name, release date, metacritic, playtime
        # If any field is missing, use a fallback (e.g., 'N/A')
        name = game_info.get("name", "N/A")
        released = game_info.get("released", "N/A")
        metacritic = game_info.get("metacritic", "N/A")
        playtime = game_info.get("playtime", "N/A")
        return [name, released, metacritic, playtime]