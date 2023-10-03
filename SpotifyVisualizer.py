import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv('./.env')
ClientID=os.getenv("ClientID")
Clientsecret=os.getenv("Clientsecret")


def main():
    print('hello')

if __name__ == "__main__":
    main()