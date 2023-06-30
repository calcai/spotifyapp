from dotenv import load_dotenv
import os
import base64
from pip._vendor.requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data= {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists")
        return None
    else:
        return json_result[0]

def get_artist_stats(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)
    popularity = json_result["popularity"]
    followers = json_result["followers"]["total"]
    genres = json_result["genres"]
    return [popularity, followers, genres]
    
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album&market=US&limit=50"
    headers = get_auth_header(token)
    result = get(url,headers = headers)
    json_result = json.loads(result.content)["items"]
    return json_result

def get_similar_artists(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["artists"]
    return json_result

artist = input("Search an artist: \n")

token = get_token()
result = search_for_artist(token, artist)
artist_id = result["id"]
stats = get_artist_stats(token, artist_id)
popularity = stats[0]
followers = stats[1]
genres = ", ".join(stats[2])
songs = get_songs_by_artist(token, artist_id)
albums = get_albums_by_artist(token, artist_id)
similar_artists = get_similar_artists(token, artist_id)


print(f"Popularity Score: {popularity} | Followers: {followers} | Genres: {genres}")

print("\nTop Songs:")
for i, song in enumerate(songs):
    print(f"{i + 1}. {song['name']}")    

print("\nAlbums: ")
for album in albums:
    print(f"{album['release_date']}: {album['name']}")

print("\n Similar Artists: ")
for i, artist in enumerate(similar_artists):
    print(f"{i + 1}. {artist['name']}")