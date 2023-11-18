import spotipy
from dotenv import dotenv_values
from playlist_generator import get_playlist


def get_song_titles(playlist):
    search_queries = []
    for song in playlist:
        search_queries.append(f"{song['song']} {song['artist']}")
    return search_queries

def capitalize_prompt(user_prompt):
    user_prompt = " ".join(user_word.capitalize() for user_word in user_prompt.split(" "))
    return user_prompt

def auth_spotify(playlist_scope = "private"):
    config = dotenv_values(".env")
    spotify = spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            client_id=config["SPOTIFY_CLIENT_ID"],
            client_secret=config["SPOTIFY_CLIENT_SECRET"],
            redirect_uri="http://localhost:9999",
            #determines what a user can do after logging in
            scope="playlist-modify-private" if playlist_scope == "private" else "playlist-modify-public"
        )
    )
    return spotify


def create_empty_playlist(spotify:object, current_user, title:str): #title == user_prompt
    created_playlist = spotify.user_playlist_create(
        current_user["id"],
        public=False,
        name = title
    )
    return created_playlist

def get_playlist_songs(spotify, search_results = None):
    '''returns a list of song ids from the search results'''
    # results_len = len(search_results["tracks"]["items"])
    print(len(search_results), search_results)
    tracks = [search_results["tracks"]["items"][0]["id"]]
    # search_results = spotify.search(q="Uptown Funk", type = "track", limit=10)
    # results_len = len(search_results["tracks"]["items"])
    # tracks = ([search_results["tracks"]["items"][num]["id"] for num in range(results_len)])
    print(tracks)
    return tracks

def get_search_queries(spotify, playlist):
    '''returns a list spotify.search object for each song in the playlist'''
    search_queries = get_song_titles(playlist)
    search_results = spotify.search(q=search_queries, type = "track", limit=len(search_queries))
    return search_results

def generate_playlist(length = None, prompt = None):
    playlist, prompt = get_playlist(length, prompt)
    spotify, user_prompt = auth_spotify(), capitalize_prompt(prompt)

    current_user = spotify.current_user()
    created_playlist = create_empty_playlist(spotify, current_user, user_prompt)
    search_queries = get_search_queries(spotify, playlist)
    tracks = get_playlist_songs(spotify, search_queries)
    spotify.user_playlist_add_tracks(current_user["id"], created_playlist["id"], tracks)

#delete .cache to log user out



# assert current_user is not Noney
#searchs for 10 songs with the name "Uptown Funk" and prints their ids

def main():
    generate_playlist()
if __name__ == "__main__":
    main()