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

#range of 0 to 100 based on listens and how recent the listens are
def getTrackPopularity(track):
    return spotify.track(track)['popularity']

#range of 0.0 to 1.0 with 1.0 being most dancable
def getTrackDanceability(track):
    return spotify.audio_features(track)[0]['danceability']

#range from -60 to 0 decibals
def getTrackLoudness(track):
    return spotify.audio_features(track)[0]['loudness']

#range from 0.0 to 1.0 describing the musical positiveness conveyed by a track (high = happy(pos), low = sad(neg))
def getTrackValence(track):
    return spotify.audio_features(track)[0]['valence']

def getTrackInstrumentalness(track):
    return spotify.audio_features(track)[0]['instrumentalness']

def main():
    
    #TODO
    #get top 5 songs from user
    #get 5 values (popularity, danceability, loudness, valence, instrumentalness)
    #create radar chart using matplotlib

    for key, value in track_id.items():
        print("Song: "+ str(key))
        print("Popularity: "       + str(getTrackPopularity(value)))
        print("Danceability: "     + str(getTrackDanceability(value)))
        print("Loudness: "         + str(getTrackLoudness(value)))
        print("Valence: "          + str(getTrackValence(value)))
        print("Instrumentalness: " + str(getTrackInstrumentalness(value)))
        print()

if __name__ == "__main__":
    main()