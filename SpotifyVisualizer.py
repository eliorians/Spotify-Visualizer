import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import pandas as pd

#load secret credentials
load_dotenv("./.env")
ClientID=os.getenv("ClientID")
Clientsecret=os.getenv("Clientsecret")


#artist IDs
artist_id= {
    "kendrickLamar": "2YZyLoL8N0Wb9xBt1NhZWg",
    "zachBryan": "40ZNYROS4zLfyyBSs2PGe2",
    "taylorSwift": "06HL4z0CvFAxyc27GXpf02",
    "lilKee" : "21UqznWenhsInMOKxpVPBd"
}

def main():

    #Authentication (without user)
    client_credentials_manager = SpotifyClientCredentials(client_id=ClientID, client_secret=Clientsecret)
    spotify = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    
    #select the artist
    artist = artist_id["kendrickLamar"]

    #artist album data into dataframe
    artistAlbums = pd.DataFrame(spotify.artist_albums(artist))
    #dataframe to csv
    artistAlbums.to_csv('./output.csv')

if __name__ == "__main__":
    main()