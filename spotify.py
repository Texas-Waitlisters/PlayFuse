import sys;
import os; 
import spotipy; 
import spotipy.util as util; 
os.environ['SPOTIPY_CLIENT_ID']='6c046a5a012c406e9677413fc844809e' 
os.environ['SPOTIPY_CLIENT_SECRET']='8f84bde73dc4477da4da9648c07885a1' 
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost/'

username = 'nhuck15';

def search(song):
    token = util.prompt_for_user_token(username,'playlist-modify-public');
    sp = spotipy.Spotify(auth=token);
    results = sp.search(song);
    print results
    vals = [];
    for x in results['tracks']['items']:
        vals.append("%s,%s,%s" % (x['name'],x['artists'][0]['name'],x['album']['name']))
    return vals;

def getPlaylist(name):
    token = util.prompt_for_user_token(username,'playlist-modify-public');
    sp = spotipy.Spotify(auth=token);
    playlists = sp.user_playlists(username)
    vals = [];
    for playlist in playlists['items']:
        print playlist['name']
        if playlist['name'] == name:
            results = sp.user_playlist(username, playlist['id'])
            tracks = results['tracks'];
            for x in tracks['items']:
                x = x['track']
                vals.append("%s,%s,%s" % (x['name'],x['artists'][0]['name'],x['album']['name']))
    return vals;

def add(song, name):
    token = util.prompt_for_user_token(username,'playlist-modify-public');
    sp = spotipy.Spotify(auth=token);
    results = sp.search(song);
    playlists = sp.user_playlists(username)
    songID = results['tracks']['items'][0]['id']
    playlistID = None;
    for playlist in playlists['items']:
        print playlist['name']
        if playlist['name'] == name:
            playlistID = playlist['id'];
    sp.user_playlist_add_tracks(username, playlistID, [songID]);

def remove(song, name):
    token = util.prompt_for_user_token(username,'playlist-modify-public');
    sp = spotipy.Spotify(auth=token);
    results = sp.search(song);
    playlists = sp.user_playlists(username)
    songID = results['tracks']['items'][0]['id']
    playlistID = None;
    for playlist in playlists['items']:
        print playlist['name']
        if playlist['name'] == name:
            playlistID = playlist['id'];
    sp.user_playlist_remove_all_occurrences_of_tracks(username, playlistID, [songID]);

def getAllPlaylists():
    token = util.prompt_for_user_token(username,'playlist-modify-public');
    sp = spotipy.Spotify(auth=token);
    playlists = sp.user_playlists(username)
    vals = [];
    for playlist in playlists['items']:
        vals.append(playlist['name'])
    return vals;

print remove('breaking the girl', 'etc')
