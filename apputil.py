# your code here ...
import pandas as pd
import requests

class Genius:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.genius.com"

    def search_song(self, song_title: str):
        """
        Searches Genius API for a song title and returns a list of matches.
        Each match contains song name, artist, and Genius URL.
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "q": song_title
        }

        # Send GET request to Genius API
        response = requests.get(f"{self.base_url}/search", headers=headers, params=params)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            print("HTTP error:", response.status_code, response.text)
            raise

        data = response.json()

        # Extract results
        hits = data.get("response", {}).get("hits", [])
        results = []
        for hit in hits:
            song_info = hit.get("result", {})
            results.append({
                "title": song_info.get("title"),
                "artist": song_info.get("primary_artist", {}).get("name"),
                "url": song_info.get("url")
            })

        return results
    
    def get_artist(self, artist_name: str):
        """
        Gets Genius artist info by name, returns a dictionary.
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {"q": artist_name}
        
        # Step 1: Search to get artist ID
        response = requests.get(f"{self.base_url}/search", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        hits = data.get("response", {}).get("hits", [])
        if not hits:
            return None

        artist_id = hits[0].get("result", {}).get("primary_artist", {}).get("id")
        
        # Step 2: Call artist endpoint for full details
        response = requests.get(f"{self.base_url}/artists/{artist_id}", headers=headers)
        response.raise_for_status()
        artist_data = response.json().get("response", {}).get("artist", {})
        
        return {
            "artist_name": artist_data.get("name"),
            "artist_id": artist_data.get("id"),
            "followers_count": artist_data.get("followers_count")
        }


    def get_artists(self, search_terms: list):
        """
        Takes a list of search terms and returns a DataFrame with:
        search_term, artist_name, artist_id, followers_count
        """
        rows = []
        for term in search_terms:
            info = self.get_artist(term)
            if info:
                rows.append({
                    "search_term": term,
                    "artist_name": info.get("artist_name"),
                    "artist_id": info.get("artist_id"),
                    "followers_count": info.get("followers_count")
                })
            else:
                rows.append({
                    "search_term": term,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                })

        return pd.DataFrame(rows)
    
