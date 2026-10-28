import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
SPOTIPY_CLIENT_ID = '0e1c86ddb99941ee8340882cd54816cb'
SPOTIPY_CLIENT_SECRET = 'b0bd586caf004e3aa82615bbde4b07f5'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/callback'

# Set up Spotify OAuth
scope = 'user-read-playback-state,user-modify-playback-state'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

# Function to play a song
def play_song(song_name, artist_name):
    results = sp.search(q=f'{song_name} {artist_name}', type='track')
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris=[track_uri])
        print(f'Playing {song_name} by {artist_name}')
    else:
        print(f'Song not found: {song_name} by {artist_name}')

# Function to pause playback
def pause_playback():
    sp.pause_playback()
    print('Playback paused')

# Function to resume playback
def resume_playback():
    sp.start_playback()
    print('Playback resumed')

# Example usage
play_song('Happy', 'Pharrell Williams')
pause_playback()
resume_playback()