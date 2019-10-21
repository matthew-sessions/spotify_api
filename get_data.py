import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2


def get_songs(song):
    CLIENT_ID = "2f444856f43c47f6ba712993205ae254"
    CLIENT_SECRET = "9757ea527ba14afc974f8c3ecb09458f"

    credentials = oauth2.SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET)

    token = credentials.get_access_token()
    spotify = spotipy.Spotify(auth=token)

    track = "coldplay yellow"
    songs = spotify.search(song, limit=7, offset=0, type='track', market='US')
    tracks = []
    for i in songs['tracks']['items']:
      tracks.append({'song_name':i['name'], 'artist':i['artists'][0]['name'], 'id':i['id']})
    return(tracks)

def get_features(id):
    CLIENT_ID = "2f444856f43c47f6ba712993205ae254"
    CLIENT_SECRET = "9757ea527ba14afc974f8c3ecb09458f"

    credentials = oauth2.SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET)

    token = credentials.get_access_token()
    spotify = spotipy.Spotify(auth=token)

    feat = spotify.audio_features(tracks=id)
    pop = spotify.track(id)
    i = feat[0]
    feat_dict = {'acousticness':i['acousticness'], 'danceability':i['danceability'],'duration_ms':i['duration_ms'],
                'energy':i['energy'], 'instrumentalness':i['instrumentalness'], 'key':i['key'],'liveness':i['liveness'],
                'loudness':i['loudness'], 'mode':i['mode'], 'speechiness':i['speechiness'], 'tempo':i['tempo'],
                'time_signature':i['time_signature'], 'valence':i['valence'], 'popularity':pop['popularity']}
    return(feat_dict)
