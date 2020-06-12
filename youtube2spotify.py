#!/usr/bin/env python
# coding: utf-8

# To obtain your client_id and client_secret - goto https://developer.spotify.com/dashboard/applications 
# and create a 'New App'.
# In the app setting - Set redirect URL to 'http://example.com'. 

# spotify_user_id is your spotify username. 
#Go here to check 'https://www.spotify.com/sg-en/account/overview/'

import sys
import requests
import json
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl
import click

#@click.command()
class youtube2spotify(object):
 
   
    def __init__(self,client_id, client_secret, spotify_user_id):
        # for spotify
        self.client_id = client_id
        self.client_secret = client_secret
        self.spotify_user_id = spotify_user_id

        self.redirect_uri = 'http://example.com' #set this to whatever you set in https://developer.spotify.com/dashboard/applications
        self.scope = 'playlist-modify-private'
        self.spotify_token = self.get_user_token()
        self.playlist_id = None 
        self.uri = []

        # for youtube
        self.scopes = ['https://www.googleapis.com/auth/youtube.readonly']
        self.auth_response = self.youtube_auth()
        
        self.liked_videos = []
        self.all_songs_info = {}
        
    
    def get_user_token(self): # function to get spotify user token
        
        query = "https://accounts.spotify.com/authorize?client_id={}&redirect_uri={}&scope={}&response_type=token".format(self.client_id,self.redirect_uri, self.scope)
        print("Please open {} in your webbrowser to grant access".format(query))
        url = input("Please paste the URL that you were redirected to: ")
        try:
            temp = url.split('token=')[1]
            token = temp.split('&token')[0]
            self.spotify_token = token
            return token
        except:
            raise Exception("The URL entered is wrong")
    
    def create_playlist(self): # function to create spotify playlist

        request_body = json.dumps({
        "name": "Youtube Liked Vids",
        "description": "All Liked Youtube Videos",
        "public": False
        })
        
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.spotify_user_id)
        r = requests.post(query, data=request_body, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)})

        if r.status_code in range (200,300):
            self.playlist_id = r.json()['id'] 
            print ("Sucessful in  Creating your Playlist ID {}".format(self.playlist_id))
            return
        
        raise Exception("Something went wrong in authenticating to Spotify")

        
    def search_songs(self):
        for i in self.all_songs_info:
            artist = self.all_songs_info[i]['artist']
            song_name = self.all_songs_info[i]['song_name']
            query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&offset=0&limit=20".format(
            song_name,
            artist
            )
            response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
                }
            )
            response_json = response.json() # returns a dict
            
            try:
                songs = response_json["tracks"]["items"] # returns a list. 
            # only use the first song
                self.uri.append(songs[0]["uri"]) #If song not found then continue
            except:
                continue
        
    
    
    def add_songs(self):
        self.get_liked_videos()
        
        if not self.playlist_id:
            self.create_playlist()
        
        if not self.uri:
            self.search_songs()
                
        for u in self.uri:
            query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.playlist_id ,u)
            r = requests.post(query, 
            headers = {
                  "Content-Type": "application/json",
                  "Authorization": "Bearer {}".format(self.spotify_token)
        })
            
         
        if r.status_code in range (200,300):
            print ("Sucessfully added songs to your playlist")
                 
        else:   
            raise Exception("Something went wrong in adding Songs to the Playlist")
    
    
    
    def youtube_auth(self): # Copied from google API docs
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, self.scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        return youtube 

    
    def get_liked_videos(self): 
        # get liked videos and append to a list. Copied from google API docs
        request = self.auth_response.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )
        response = request.execute() #returns a dict
        
        for i in response['items']: 
            if i not in self.liked_videos:
                self.liked_videos.append(i['id'])
        
        if self.liked_videos:    
            self.get_video_info()
        else:
            raise Exception("No Video's liked")
    
    def get_video_info(self):
        # get list of liked videos and add information about artist and song. Save to a dict 
        for l in self.liked_videos:
            youtube_url = "https://www.youtube.com/watch?v={}".format(l)
                
            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
            video_title = video["title"]
            song_name = video["track"]
            artist = video["artist"]
              
            if song_name is not None and artist is not None:
            # save all important info and skip any missing song and artist
                self.all_songs_info[video_title] = {
                    "youtube_url": youtube_url,
                    "song_name": song_name,
                    "artist": artist
            }

if __name__ == '__main__':
	a = youtube2spotify(sys.argv[1] , sys.argv[2] , sys.argv[3])
	a.add_songs()