import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Deine Daten vom Spotify Developer Dashboard
scope = "user-library-read user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="DEINE_ID",
    client_secret="DEIN_SECRET",
    redirect_uri="http://localhost:8080/callback",
    scope=scope
))

# Test: Welcher Song läuft gerade?
current = sp.current_playback()
if current:
    print(f"Gerade läuft: {current['item']['name']}")