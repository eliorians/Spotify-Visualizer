import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import pandas as pd

#DOCUMENTATION:
#https://developer.spotify.com/documentation/web-api

#load secret credentials
load_dotenv("./.env")
ClientID=os.getenv("ClientID")
Clientsecret=os.getenv("Clientsecret")
#Authentication (without user)
client_credentials_manager = SpotifyClientCredentials(client_id=ClientID, client_secret=Clientsecret)
spotify = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#artist IDs
artist_id= {
    "kendrickLamar" : "2YZyLoL8N0Wb9xBt1NhZWg",
    "zachBryan"     : "40ZNYROS4zLfyyBSs2PGe2",
    "taylorSwift"   : "06HL4z0CvFAxyc27GXpf02",
    "lilKee"        : "21UqznWenhsInMOKxpVPBd"
}

#track IDs
track_id= {
    "revival"       : "2QfX9Pdz3q66fN3kCXl0Js",
    "money trees"   : "2HbKqm4o0w5wEeEFXm2sD4"
}

def getTrackPopularity(track):
    return spotify.track(track)['popularity']

def getTrackDanceability(track):
    return spotify.audio_features(track)[0]['danceability']


def main():
    
    for key, value in track_id.items():
        print("Song: "+ str(key))
        print("Popularity: "   + str(getTrackPopularity(value)))
        print("Danceability: " + str(getTrackDanceability(value)))
        print()


if __name__ == "__main__":
    main()