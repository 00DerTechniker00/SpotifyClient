import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

success = load_dotenv()

print(f"--- Debug Infos ---")
print(f"Arbeitsverzeichnis: {os.getcwd()}")
print(f".env Datei gefunden & geladen: {success}")

meine_id = os.getenv("SPOTIPY_CLIENT_ID")
mein_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
print(f"Client ID: {meine_id}")
print(f"Client Secret: {mein_secret}")

try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-read-currently-playing"))
    
    user_info = sp.current_user()
    print(f"Erfolgreich eingeloggt als: {user_info['display_name']}")
    
except Exception as e:
    print(f"Fehler beim Login: {e}")