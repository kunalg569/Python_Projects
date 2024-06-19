import json
import os # For importing environment variables
import spotipy
from spotipy import SpotifyClientCredentials
import boto3 # By AWS to programatically communicate with AWS services
from datetime import datetime


def lambda_handler(event, context):
    
    # Environment variable 1 and 2
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    
    # Provide secret key and client key id:
    client_credential_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
    
    # Objects to extract data from spotify website:
    sp = spotipy.Spotify(client_credentials_manager= client_credential_manager)
    playlists = sp.user_playlists('spotify') 
    
    # Extract playlist URI from the top 100 treding songs spotify website
    playlist_link = 'https://open.spotify.com/playlist/5ABHKGoOzxkaa28ttQV9sE'
    playlist_URI = playlist_link.split('/')[-1]
    
    data = sp.playlist_tracks(playlist_URI)
    # Test Code: print(data)
    
    # Storing data into s3 bucket
    client = boto3.client('s3')
    
    filename = "spotify_raw_" + str(datetime.now()) + ".json"
    
    client.put_object(
        Bucket = 'spotify-etl-project-dawny',       # bucket name
        Key = 'raw_data/data_to_be_processed/' + filename,     # folder where you want to store
        Body = json.dumps(data)                      # dumping data 
        )   
        
