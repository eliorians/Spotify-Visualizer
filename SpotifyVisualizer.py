import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

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

#generates a random color
def generate_random_color():
    # Generate random values for red, green, and blue components
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    # Ensure significantly different colors by increasing the range of random values
    if random.random() < 0.5:
        red = random.randint(150, 255)
    if random.random() < 0.5:
        green = random.randint(150, 255)
    if random.random() < 0.5:
        blue = random.randint(150, 255)

    # Convert RGB to hexadecimal format
    hex_color = "#{:02x}{:02x}{:02x}".format(red, green, blue)

    # Return the random color in hexadecimal format
    return hex_color

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

#scale the value from -60-0 to 0-100
def scaleLoudness(x):
    return ((x - (-60)) / (0 - (-60))) * (100 - 0) + 0

#scale the value from 0-1 to 0-100
def scaleOther(x):
    return x * 100

def getValues(trackID):
    values = [] 
    values.append(getTrackPopularity(trackID))
    values.append(scaleOther(getTrackDanceability(trackID)))
    values.append(scaleLoudness(getTrackLoudness(trackID)))
    values.append(scaleOther(getTrackValence(trackID)))
    values.append(scaleOther(getTrackEnergy(trackID)))
    return values

#takes a list of 5 values to be plotted
def buildRadar(values, names):
    labels = ['popularity', 'danceability', 'loudness', 'valence', 'energy']
    num_vars = len(labels) 

    # Split the circle into even parts and save the angles so we know where to put each axis.
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Helper function to plot each car on the radar chart.
    def add_to_radar(song_name, color, value):
        # The plot is a circle, so we need to "complete the loop" and append the start value to the end.
        value += value[:1]
        # Draw the outline of our data.
        ax.plot(angles, value, color=color, linewidth=1, label=song_name)
        # Fill it in.
        ax.fill(angles, value, color=color, alpha=0.25)
    
    for i in range(len(values)):
        add_to_radar(names[i], generate_random_color(), values[i])

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

#returns list of all track ids in a playlist
def getPlaylistTrackIDs(playlist):
    playlistTracks = spotify.playlist_tracks(playlist)['items']
    playlistTrackIDs = []
    for i in playlistTracks:
        track = i['track']
        playlistTrackIDs.append(track['id'])

    return playlistTrackIDs

#returns list of all track names in a playlist
def getPlaylistTrackNames(playlist):
    playlistTracks = spotify.playlist_tracks(playlist)['items']
    playlistTrackNames = []
    for i in playlistTracks:
        track = i['track']
        playlistTrackNames.append(track['name'])

    return playlistTrackNames

def main():

    playlist_link = 'https://open.spotify.com/playlist/5OWeSaYktfEI313ue6ms1d'
    #playlist_link = input("Enter a link to a playlist: ")    
    playlist_link = playlist_link.rsplit('/', 1)[-1]
    playlist_track_ids =  getPlaylistTrackIDs(playlist_link)
    playlist_track_names =  getPlaylistTrackNames(playlist_link)

    valuesList = []
    for i in playlist_track_ids:
        valuesList.append(getValues(i))

    buildRadar(valuesList, playlist_track_names)

    #radar plot testing
    #value = track_id["revival"]
    #values = [getTrackPopularity(value), scaleOther(getTrackDanceability(value)), scaleLoudness(getTrackLoudness(value)), scaleOther(getTrackValence(value)), scaleOther(getTrackEnergy(value))]
    #buildRadar(values)

    #song value testing
    # for key, value in track_id.items():
    #     print("Song: "+ str(key))
    #     print("Popularity: "   + str(getTrackPopularity(value)))
    #     print("Danceability: " + str(getTrackDanceability(value)))
    #     print("Loudness: "     + str(getTrackLoudness(value)))
    #     print("Valence: "      + str(getTrackValence(value)))
    #     print("Energy: "       + str(getTrackEnergy(value)))
    #     print()

if __name__ == "__main__":
    main()
