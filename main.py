from bs4 import BeautifulSoup
import requests
import lxml

user_input = input("Enter the Date in YYYY-MM-DD- ")
website = requests.get(f'https://www.billboard.com/charts/hot-100/{user_input}/').text
soup = BeautifulSoup(website, 'lxml')

songs = soup.select(selector='span.a-no-trucate')
all_songs = [song.getText().strip() for song in songs]
print(all_songs)
