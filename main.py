from bs4 import BeautifulSoup
import requests
import lxml
import spotipy
from spotipy.oauth2 import SpotifyOAuth

user_input = input("Enter the Date in YYYY-MM-DD- ")
website = requests.get(f'https://www.billboard.com/charts/hot-100/{user_input}/').text
soup = BeautifulSoup(website, 'lxml')

songs = soup.select(selector='span.a-no-trucate')
all_songs = [song.getText().strip() for song in songs]

with open('user.txt') as f:
    user = f.readlines()

user_ele = [ele.split("=")[1].strip() for ele in user]
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com",
        client_id=user_ele[0],
        client_secret=user_ele[1],
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = user_input.split("-")[0]
for song in all_songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{user_input} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)