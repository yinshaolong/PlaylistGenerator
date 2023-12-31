import spotipy
from dotenv import dotenv_values
from playlist_generator import get_playlist, parse_args, logout_user


def get_song_titles(playlist):
    search_queries = []
    for song in playlist:
        search_queries.append(f"{song['song']} {song['artist']}")
    return search_queries

def capitalize_prompt(user_prompt):
    user_prompt = " ".join(user_word.capitalize() for user_word in user_prompt.split(" "))
    return user_prompt

def auth_spotify(playlist_scope = "public"):
    config = dotenv_values(".env")
    scope = "playlist-modify-private" if playlist_scope == "private" else 'playlist-modify-public' # playlist-modify-public insuffiecient client scope
    spotify = spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            client_id=config["SPOTIFY_CLIENT_ID"],
            client_secret=config["SPOTIFY_CLIENT_SECRET"],
            redirect_uri="http://localhost:9999",
            #determines what a user can do after logging in
            scope='playlist-modify-private'
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
    tracks = [search_results[idx]["tracks"]["items"][0]["id"] for idx in range(len(search_results))]
    return tracks

def get_search_queries(spotify, playlist):
    '''returns a list spotify.search object for each song in the playlist'''
    search_queries = get_song_titles(playlist)
    search_results = [spotify.search(q=query, type = "track", limit= 3) for query in search_queries ]
    return search_results

def create_spotify_playlist(playlist, prompt)->None:
    #check to see if playlist is private or public
    priv_or_public = parse_args().pop 
    priv_or_public = priv_or_public if priv_or_public == "private" else "public"
    #Get spotify user acc info in .cache and capitalize the prompt as the playlist title (user_prompt)
    spotify, user_prompt = auth_spotify(priv_or_public), capitalize_prompt(prompt)
    #create empty playlist
    current_user = spotify.current_user()
    created_playlist = create_empty_playlist(spotify, current_user, user_prompt)
    #get queries (song titles) in a format that spotify can use to search i.e. spotify.search(q=<song query>, type = "track", limit= #)
    search_queries = get_search_queries(spotify, playlist)
    #get song ids from search results
    tracks = get_playlist_songs(spotify, search_queries)
    #add songs to playlist based on song id.
    spotify.user_playlist_add_tracks(current_user["id"], created_playlist["id"], tracks)

def create_youtube_playlist(playlist, prompt):
    pass

def generate_playlist(length = None, prompt = None):
    #get json of the prompt
    playlist, prompt = get_playlist(length, prompt)
    if parse_args().t == "spotify":
        create_spotify_playlist(playlist, prompt)

#delete .cache to log user out


def main():
    args = parse_args()
    if logout_user(args):
        return
    generate_playlist()
if __name__ == "__main__":
    main()