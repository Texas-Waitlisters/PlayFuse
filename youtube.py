import httplib2
import os
import sys
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools

CLIENT_SECRETS_FILE = "client_secrets.json"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
%s
with information from the Cloud Console
https://cloud.google.com/console
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                           CLIENT_SECRETS_FILE))

YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)
    flags = tools.argparser.parse_args(args=[])
    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = tools.run_flow(flow, storage, flags)
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        http=credentials.authorize(httplib2.Http()))

def build_resource(properties):
  resource = {}
  for p in properties:
    prop_array = p.split('.')
    ref = resource
    for pa in range(0, len(prop_array)):
      is_array = False
      key = prop_array[pa]
      if key[-2:] == '[]':
        key = key[0:len(key)-2:]
        is_array = True
      if pa == (len(prop_array) - 1):
        if properties[p]:
          if is_array:
            ref[key] = properties[p].split(',')
          else:
            ref[key] = properties[p]
      elif key not in ref:
        ref[key] = {}
        ref = ref[key]
      else:
        ref = ref[key]
  return resource

def removeEmptyKwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.iteritems():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def addById(client, videoId, playlistID):
    response = client.playlistItems().insert(part="snippet", body={'snippet': { 'playlistId': playlistID, 'resourceId': { 'kind': 'youtube#video', 'videoId': videoId}}}).execute()

def add(client, videoName, playlistName):
    song = getSongId(client, part='snippet', maxResults=10, q=videoName, type='video')
    playlist = getPlaylistId(playlistName, client, part='snippet,contentDetails', mine=True, maxResults=1, onBehalfOfContentOwner='', onBehalfOfContentOwnerChannel='')
    addById(client, song, playlist)

def getSongId(client, **kwargs):
    kwargs = removeEmptyKwargs(**kwargs)
    response = client.search().list(**kwargs).execute()
    return response['items'][0]['id']['videoId']

def getPlaylistId(name, client, **kwargs): #no way to handle if playlist doesnt exist
    kwargs = removeEmptyKwargs(**kwargs)
    response = client.playlists().list(**kwargs).execute()
    result = ''
    if(response['items'][0]['snippet']['title'] == name):
        result = response['items'][0]['id']
    return result

def getSongs(client, **kwargs):
    kwargs = removeEmptyKwargs(**kwargs)
    response = client.playlistItems().list(**kwargs).execute()
    result = []
    for i in range(len(response['items'])):
        result.append(response['items'][i]['snippet']['title'])
    return result

def getPlaylist(client, playlistName):
    playlistId = getPlaylistId(playlistName, client, part='snippet,contentDetails', mine=True, maxResults=1, onBehalfOfContentOwner='', onBehalfOfContentOwnerChannel='')
    result = getSongs(client, part='snippet,contentDetails', maxResults=25, playlistId=playlistId)
    return result

def searchByKeyword(client, **kwargs):
  kwargs = removeEmptyKwargs(**kwargs)
  response = client.search().list(**kwargs).execute()
  result = []
  for x in range(0, 10):
    result.append(response['items'][x]['snippet']['title'])
  return result

def getUserPlaylists(client, **kwargs):
    kwargs = removeEmptyKwargs(**kwargs)
    response = client.playlists().list(**kwargs).execute()
    result = []
    for i in range(len(response['items'])):
        result.append(response['items'][i]['snippet']['title'])
    return result

def removeById(client, **kwargs):
  kwargs = removeEmptyKwargs(**kwargs)
  response = client.playlistItems().delete(**kwargs).execute()

def remove(client, videoName, playlistName):
    playlistId = getPlaylistId(playlistName, client, part='snippet,contentDetails', mine=True, maxResults=1, onBehalfOfContentOwner='', onBehalfOfContentOwnerChannel='')
    videoId = getVideoId(client, videoName, part='snippet,contentDetails', maxResults=25, playlistId=playlistId)
    removeById(client, id=videoId, onBehalfOfContentOwner='')

def getVideoId(client, name, **kwargs):
    kwargs = removeEmptyKwargs(**kwargs)
    response = client.playlistItems().list(**kwargs).execute()
    result = ''
    for i in range(len(response['items'])):
        if(response['items'][i]['snippet']['title'] == name):
            result = response['items'][i]['id']
    return result

def getAllPlaylists(client):
    return getUserPlaylists(client, part='snippet,contentDetails', mine=True, maxResults=10, onBehalfOfContentOwner='', onBehalfOfContentOwnerChannel='')

def search(client, query, itemType):
    result = []
    if(itemType == 'video'):
        result = searchByKeyword(client, part='snippet', maxResults=10, q=query, type='video')
    else:
        result = searchByKeyword(client, part='snippet', maxResults=1, q=query, type='')
    return result

if __name__ == '__main__':
    youtube = get_authenticated_service()
