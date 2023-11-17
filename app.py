import spotipy
from dotenv import dotenv_values

config = dotenv_values(".env")

spotify = spotipy.Spotify(
    auth_manager=spotipy.SpotifyOAuth(
        client_id=config["SPOTIFY_CLIENT_ID"],
        client_secret=config["SPOTIFY_CLIENT_SECRET"],
        redirect_uri="http://localhost:9999"
    )
)

current_user = spotify.current_user()
print(current_user)