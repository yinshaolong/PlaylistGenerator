import spotipy
from dotenv import dotenv_values
from playlist_generator import get_playlist

config = dotenv_values(".env")

spotify = spotipy.Spotify(
    auth_manager=spotipy.SpotifyOAuth(
        client_id=config["SPOTIFY_CLIENT_ID"],
        client_secret=config["SPOTIFY_CLIENT_SECRET"],
        redirect_uri="http://localhost:9999",
        #determines what a user can do after logging in
        scope="playlist-modify-private",
        # scope="playlist-modify-public"
    )
)

current_user = spotify.current_user()
# print(current_user)

#delete .cache to log user out

assert current_user is not None
#searchs for 10 songs with the name "Uptown Funk" and prints their ids
search_results = spotify.search(q="Uptown Funk", type = "track", limit=10)
results_len = len(search_results["tracks"]["items"])
print([search_results["tracks"]["items"][num]["id"] for num in range(results_len)])

#creates playlist
spotify.user_playlist_create(
    current_user["id"],
    public=False,
    name="Testing Playlist"
)