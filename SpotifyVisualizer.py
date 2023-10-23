import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

#range from 0.0 to 1.0 representing the measure of intensity
def getTrackEnergy(track):
    return spotify.audio_features(track)[0]['energy']

def scaleLoudness(x):
    return ((x - (-60)) / (0 - (-60))) * (100 - 0) + 0

def scaleOther(x):
    return x * 100

def buildRadar(values):
    labels = ['popularity', 'danceability', 'loudness', 'valence', 'energy']
    num_vars = len(labels) 

    # Split the circle into even parts and save the angles so we know where to put each axis.
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
   
    # The plot is a circle, so we need to "complete the loop" and append the start value to the end.
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Draw the outline of our data.
    ax.plot(angles, values, color='red', linewidth=1)
    # Fill it in.
    ax.fill(angles, values, color='red', alpha=0.25)

    # Fix axis to go in the right order and start at 12 o'clock.
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw axis lines for each angle and label.
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    
    # Go through labels and adjust alignment based on where it is in the circle.
    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')
    
    # Ensure radar goes from 0 to 100.
    ax.set_ylim(0, 100)
    # Set position of y-labels (0-100) to be in the middle of the first two axes.
    ax.set_rlabel_position(180 / num_vars)

    plt.show()


def main():
        
    #todo get top 5 songs from user
    #get 5 values (popularity, danceability, loudness, valence, tempo)
    #create radar chart using matplotlib
    
    value = track_id["revival"]
    values = [getTrackPopularity(value), scaleOther(getTrackDanceability(value)), scaleLoudness(getTrackLoudness(value)), scaleOther(getTrackValence(value)), scaleOther(getTrackEnergy(value))]
    buildRadar(values)

    for key, value in track_id.items():
        print("Song: "+ str(key))
        print("Popularity: "   + str(getTrackPopularity(value)))
        print("Danceability: " + str(getTrackDanceability(value)))
        print("Loudness: "     + str(getTrackLoudness(value)))
        print("Valence: "      + str(getTrackValence(value)))
        print("Energy: "       + str(getTrackEnergy(value)))
        print()


if __name__ == "__main__":
    main()