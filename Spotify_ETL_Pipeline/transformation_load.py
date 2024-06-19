import json
import boto3 
import pandas as pd             # Add pandas function as a layer since AWS does not offer this
from datetime import datetime
from io import StringIO         # For converting the dataframe into a string file

# Write the lambda_handler function first
# Then write the python transformation functions from .ipynb 


def albums(data):
    album_list = []
    for row in data['items']:
        album_id = row['track']['album']['id']
        album_name = row['track']['album']['name']
        album_release_date = row['track']['album']['release_date']
        album_total_tracks = row['track']['album']['total_tracks']
        album_url = row['track']['album']['external_urls']['spotify']
        album_element = {'album_id':album_id,'name':album_name,'release_date':album_release_date,
                            'total_tracks':album_total_tracks,'url':album_url}
        album_list.append(album_element)
    return album_list
    
    
def artists(data):
    artist_list = []
    for row in data['items']:
        for key, value in row.items():
            if key == "track":
                for artist in value['artists']:
                    artist_dict = {'artist_id':artist['id'], 'artist_name':artist['name'], 'external_url': artist['href']}
                    artist_list.append(artist_dict)
    return artist_list
        
        
def songs(data):
    song_list = []
    for row in data['items']:
        song_id = row['track']['id']
        song_name = row['track']['name']
        song_duration = row['track']['duration_ms']
        song_url = row['track']['external_urls']['spotify']
        song_popularity = row['track']['popularity']
        song_added = row['added_at']
        album_id = row['track']['album']['id']
        artist_id = row['track']['album']['artists'][0]['id']
        song_element = {'song_id':song_id,'song_name':song_name,'duration_ms':song_duration,'url':song_url,
                        'popularity':song_popularity,'song_added':song_added,'album_id':album_id,
                        'artist_id':artist_id
                       }
        song_list.append(song_element)
    return song_list
    

def lambda_handler(event, context):
    # Initialize an S3 client to interact with AWS S3
    s3 = boto3.client('s3')
    
    # Specify the S3 bucket name
    Bucket = 'spotify-etl-project-dawny'
    # Specify the prefix (directory path) within the bucket
    Key = 'raw_data/data_to_be_processed/'
    
    # List all objects within the specified bucket and prefix
    # Print the metadata of all objects under the specified prefix
    #print(s3.list_objects(Bucket=Bucket, Prefix=Key))
    
    # Print the 'Contents' key, which contains the list of objects (files)
    #print(s3.list_objects(Bucket=Bucket, Prefix=Key)['Contents'])
    
    # Iterate over each object (file) under 'Contents'
    for file in s3.list_objects(Bucket=Bucket, Prefix=Key)['Contents']:
        
        # Extract the key (file path) of the current file
        file_key = file['Key']
        # Print the file extension of the current file
        #print(file_key.split('.')[-1])
        
        # Creating empty list to store data and keys
        spotify_data = []
        spotify_key = []
        # Check if the current file is a JSON file
        if file_key.split('.')[-1] == "json":
            response = s3.get_object(Bucket=Bucket, Key=file_key)   # Get the object (file) from S3
            content = response['Body']                              # Extract the actual data (content) of the file
            jsonObject = json.loads(content.read())                 # Read the content and load it as a JSON object
            # Print the JSON object (for debugging purposes)
            #print(jsonObject)
            spotify_data.append(jsonObject)
            spotify_key.append(file_key)
            
    for data in spotify_data:
        # creating dictionary from respective functions of albums, artists, songs
        album_list = albums(data)
        artist_list = artists(data)
        song_list = songs(data)
        # Creating dataframes 
        album_df = pd.DataFrame.from_dict(album_list)
        song_df = pd.DataFrame.from_dict(song_list)
        artist_df = pd.DataFrame.from_dict(artist_list)
        # Dropping Duplicates
        song_df = song_df.drop_duplicates()
        artist_df = artist_df.drop_duplicates()
        album_df = album_df.drop_duplicates()
        # Modifying data types
        if 'release_date' in album_df.columns:
            try:
                album_df['release_date'] = pd.to_datetime(album_df['release_date'], errors='coerce', format='%Y-%m-%d')
            except ValueError:
                album_df['release_date'] = pd.to_datetime(album_df['release_date'], errors='coerce')
    
        if 'song_added' in song_df.columns:
            try:
                song_df['song_added'] = pd.to_datetime(song_df['song_added'], errors='coerce', format='%Y-%m-%d')
            except ValueError:
                song_df['song_added'] = pd.to_datetime(song_df['song_added'], errors='coerce')
        
        
        # Now you want to push this transformed data into respective S3 bucket of your choice
        
        # First create a unique name for the each file:
        song_key = "transformed_data/songs_data/songs_transformed_" + str(datetime.now()) + ".csv"
        # Creating StringIO object for transforming our songs Dataframe
        song_buffer = StringIO()
        song_df.to_csv(song_buffer, index = False)
        song_content = song_buffer.getvalue()
        s3.put_object(Bucket = Bucket, Key = song_key, Body = song_content)
        
        # Creating StringIO object for transforming our album Dataframe
        album_key = "transformed_data/album_data/album_transformed_" + str(datetime.now()) + ".csv"
        # Creating StringIO object for transforming album Dataframe
        album_buffer = StringIO()
        album_df.to_csv(album_buffer, index = False)
        album_content = album_buffer.getvalue()
        s3.put_object(Bucket = Bucket, Key = album_key, Body = album_content)
        
        # Creating StringIO object for transforming our artist Dataframe
        artist_key = "transformed_data/artist_data/artist_transformed_" + str(datetime.now()) + ".csv"
        # Creating StringIO object for transforming artist Dataframe
        artist_buffer = StringIO()
        artist_df.to_csv(artist_buffer, index = False)
        artist_content = artist_buffer.getvalue()
        s3.put_object(Bucket = Bucket, Key = artist_key, Body = artist_content)
        
    # This code moves data from to_processed folder -> processed folder deleting it from to_processed folder 
    s3_resource = boto3.resource('s3')
    for key in spotify_key:
        copy_source = {
            'Bucket': Bucket,
            'Key': key
        }
        s3_resource.meta.client.copy(copy_source, Bucket, 'raw_data/data_processed/' + key.split("/")[-1])    
        s3_resource.Object(Bucket, key).delete()