from gmusicapi import Mobileclient
api = None

def search(song):
    global api
    dict = api.search(song, 10)
    song_info = dict.get('song_hits')
    result = []
    for answers in range(0, 10):
        track = song_info[answers]['track']
        item = track['title'] + ',' + track['artist'] + ',' + track['album']
        result.append(item)
    return result

def getAllPlaylists():
    global api
    list = api.get_all_user_playlist_contents()
    result = []
    for x in range(len(list)):
        result.append(list[x]['name'])
    return result

def getPlaylist(name):
    global api
    list = api.get_all_user_playlist_contents()
    result = []
    for playlist in range(len(list)):
        if(list[playlist]['name'] == name):
            songs = list[playlist]['tracks']
            for song in songs:
                track_info = song['track']
                item = track_info['title'] + ',' + track_info['artist'] + ',' + track_info['album']
                result.append(item)
    return result

def add(song_name, playlist_name):
    global api
    list = api.get_all_user_playlist_contents() #get playlist id
    for playlist in range(len(list)):
        if(list[playlist]['name'] == playlist_name):
            p_id = list[playlist]['id']
    dict = api.search(song_name, 0) #get song id
    song_info = dict.get('song_hits')
    s_id = song_info[0]['track']['storeId']
    print(p_id)
    print(s_id)
    api.add_songs_to_playlist(p_id, s_id)

def remove(song_name, playlist_name):
    global api
    list = api.get_all_user_playlist_contents()
    for playlist in range(len(list)):
        if(list[playlist]['name'] == playlist_name):
            songs = list[playlist]['tracks']
            for song in songs:
                title = song['track']['title']
                if(title == song_name):
                    id = song['id']
                    break
    api.remove_entries_from_playlist(id);

def main():
    global api
    api = Mobileclient()
    api.logout()
    logged_in = api.login('email@gmail.com', 'pass', Mobileclient.FROM_MAC_ADDRESS)
    while(not logged_in):
        logged_in = api.login('email@gmail.com', 'pass', Mobileclient.FROM_MAC_ADDRESS)
    return api;

api = main()
api.logout()
