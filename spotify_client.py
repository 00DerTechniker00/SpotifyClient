import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

class SpotifyHandler:
    def __init__(self):
        load_dotenv()
        self.scope = "user-read-currently-playing user-library-read"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope))

    def get_current_track_info(self):
        try:
            track = self.sp.current_user_playing_track()
            if track and track['item']:
                item = track['item']
                name = f"{item['artists'][0]['name']} - {item['name']}"
                cover_url = item['album']['images'][0]['url'] if item['album']['images'] else None
                return {"name": name, "cover": cover_url}
            return None
        except Exception as e:
            print(f"Fehler beim Abrufen des aktuellen Songs: {e}")
            return None

    def get_saved_tracks(self, limit=10):
        try:
            results = self.sp.current_user_saved_tracks(limit=limit)
            return [f"{item['track']['artists'][0]['name']} - {item['track']['name']}"
                    for item in results['items']]
        except Exception as e:
            return f"Fehler: {e}"