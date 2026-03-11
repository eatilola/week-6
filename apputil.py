import requests
import pandas as pd


class Genius:
    """
    Simple wrapper for the Genius API.
    """

    def __init__(self, access_token):
        """
        Initialize Genius object with access token.
        """
        self.access_token = access_token
        self.base_url = "https://api.genius.com"

    def _search(self, search_term):
        """
        Private helper function to search Genius API.
        """
        url = f"{self.base_url}/search"
        params = {
            "q": search_term,
            "access_token": self.access_token
        }

        response = requests.get(url, params=params)
        data = response.json()

        return data["response"]["hits"]

    def get_artist(self, search_term):
        """
        Get artist information from Genius API.

        Parameters
        ----------
        search_term : str
            Artist name to search

        Returns
        -------
        dict
            JSON dictionary containing artist information
        """

        hits = self._search(search_term)

        if len(hits) == 0:
            return None

        # get artist id from first hit
        artist_id = hits[0]["result"]["primary_artist"]["id"]

        # pull artist info
        artist_url = f"{self.base_url}/artists/{artist_id}"
        params = {"access_token": self.access_token}

        response = requests.get(artist_url, params=params)
        artist_data = response.json()

        return artist_data["response"]["artist"]

    def get_artists(self, search_terms):
        """
        Get artist information for multiple search terms.

        Parameters
        ----------
        search_terms : list
            List of artist names

        Returns
        -------
        pandas.DataFrame
        """

        rows = []

        for term in search_terms:
            artist = self.get_artist(term)

            if artist is None:
                rows.append({
                    "search_term": term,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                })
                continue

            rows.append({
                "search_term": term,
                "artist_name": artist.get("name"),
                "artist_id": artist.get("id"),
                "followers_count": artist.get("followers_count")
            })

        return pd.DataFrame(rows)