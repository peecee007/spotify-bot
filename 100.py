import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# Spotify API credentials
SPOTIPY_CLIENT_ID = 'your-spotify-client-id'
SPOTIPY_CLIENT_SECRET = 'your-spotify-client-secret'
SPOTIPY_REDIRECT_URI = 'your-app-redirect-url'

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

# Function to simulate streams
def simulate_streams(song_name, artist_name, num_streams, duration):
    for i in range(num_streams):
        play_song(song_name, artist_name)
        time.sleep(duration)  # Wait for the specified duration
        sp.pause_playback()  # Pause playback to reset the stream
        time.sleep(1)  # Wait for 1 second before starting the next stream
        print(f'Stream {i+1} completed')

# Example usage
song_name = 'Happy'
artist_name = 'Pharrell Williams'
num_streams = 100
duration = 30  # Play each song for 30 seconds
simulate_streams(song_name, artist_name, num_streams, duration)