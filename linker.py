from flask import Flask, jsonify, request, render_template
import spotify;
import googlemusic;
app = Flask(__name__)

currentgPlaylist = None;
currentsPlaylist = None;

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getPlaylists', methods = ['POST'])
def getPlaylist():
    username = request.form['username']
    password = request.form['password']
    platform = request.form['platform']
    print('%s %s %s' % (username, password, platform))
    if username and password and platform:
        list = None;
        print(platform)
        if platform == 'google music':
            googlemusic.setup(username,password)
            list = googlemusic.getAllPlaylists()
            print("aaaaa")
        if platform == 'spotify':
            list = spotify.getAllPlaylists()
        print(list)
        return jsonify({'playlists' : list})
    return jsonify({'playlists' : []})

@app.route('/loadSongs', methods = ['POST'])
def loadSongs():
    playlistName = request.form['playlistName']
    username = request.form['username']
    password = request.form['password']
    platform = request.form['platform']
    if username and password and platform and playlistName:
        list = None;
        if platform == 'google music':
            googlemusic.setup(username,password)
            list = googlemusic.getPlaylist(playlistName)
        if platform == 'spotify':
            list = spotify.getPlaylist(playlistName)
        return jsonify({'songs' : list})
    return jsonifiy({'songs' : []})

@app.route('/search', methods = ['POST'])
def search():
    songName = request.form['songName']
    susername = request.form['susername']
    spassword = request.form['spassword']
    gusername = request.form['gusername']
    gpassword = request.form['gpassword']
    googlemusic.setup(gusername,gpassword)
    list1 = [];
    if gusername and gpassword:
        list1 = googlemusic.search(songName)
    list2 = [];
    if susername and spassword:
            list2 = spotify.search(songName)
    list = [];
    for i in range(min(len(list1),len(list2))):
        list.append({'track': list1[i], 'platform' : 'google music'});
        list.append({'track': list2[i], 'platform' : 'spotify'});
    return jsonify({'songs' : list})

#TODO: ADD and REMOVE
@app.route('/add', methods = ['POST'])
def add():
    track = request.form['track']
    username = request.form['username']
    password = request.form['password']
    platform = request.form['platform']
    playlist = request.form['playlist']
    if username and password and platform and playlist:
        track = track.split(",")[0];
        list = None;
        if platform == 'google music':
            googlemusic.setup(username,password)
            list = googlemusic.add(track, playlist)
        if platform == 'spotify':
            list = spotify.add(track, playlist)

@app.route('/remove', methods = ['POST'])
def remove():
    track = request.form['track']
    username = request.form['username']
    password = request.form['password']
    platform = request.form['platform']
    playlist = request.form['playlist']
    if username and password and platform and playlist:
        track = track.split(",")[0];
        list = None;
        if platform == 'google music':
            googlemusic.setup(username,password)
            list = googlemusic.remove(track, playlist)
        if platform == 'spotify':
            list = spotify.remove(track, playlist)

app.run()


#print(app.post('/getPlaylists', data=dict(username='nhuck15', password=' ', platform='spotify'), follow_redirects=True))
