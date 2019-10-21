import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2
from decouple import config
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
from numpy.linalg import norm


CLIENT_ID_var = config("CLIENT_ID")
CLIENT_SECRET_var = config("CLIENT_SECRET")

#get the ids of 100 recommendations from spotify

class Five_recs:
    CLIENT_ID = CLIENT_ID_var
    CLIENT_SECRET = CLIENT_SECRET_var
    credentials = oauth2.SpotifyClientCredentials(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET)
    token = credentials.get_access_token()
    spotify = spotipy.Spotify(auth=token)
    def __init__(self,id,spotify=spotify):
      self.id = id
      self.spotify = spotify

    def get_100(self):
        res = self.spotify.recommendations(seed_tracks=[self.id], limit=100)
        ids = [i['id'] for i in res['tracks']]
        return(ids)

    def get_all_features(self, list_id):
        res = self.spotify.audio_features(tracks=list_id)
        df = pd.DataFrame( columns=['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'id', 'duration_ms', 'time_signature'])

        for i in res:
            feat_dict = {'acousticness':i['acousticness'], 'danceability':i['danceability'],'duration_ms':i['duration_ms'],
                          'energy':i['energy'], 'instrumentalness':i['instrumentalness'], 'key':i['key'],'liveness':i['liveness'],
                        'loudness':i['loudness'], 'mode':i['mode'], 'speechiness':i['speechiness'], 'tempo':i['tempo'],
                        'time_signature':i['time_signature'], 'valence':i['valence'], 'id':i['id']}
            df = df.append(feat_dict,ignore_index=True)
        return(df)

    def top_recs(self,df_recs,song_df):
        df = df_recs
        Spot_Scaler = StandardScaler()
        df_scaled = Spot_Scaler.fit_transform(df.drop(['id'], axis=1))
        feats = Spot_Scaler.transform(song_df.drop(['id'], axis=1))
        df['dist'] = list(map(lambda x: norm(x-np.array(feats)[0]), np.array(df_scaled)))
        top = df.sort_values(by='dist').iloc[0:5]
        return top.drop(['dist'], axis=1)

    def feedback(self, ids):
        vals = ids.id.values
        song_info = []
        for i in vals:
            tracks = self.spotify.track(i)
            song_info.append({'large_image':tracks['album']['images'][0]['url'], 'med_image':tracks['album']['images'][1]['url'],'small_image':tracks['album']['images'][2]['url'],
                              'artist':tracks['artists'][0]['name'], 'song_name':tracks['name'], 'id':tracks['id'], 'uri':tracks['uri']})
        return(song_info)
