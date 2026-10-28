import spotipy
from spotipy.oauth2 import SpotifyOAuth
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

# Spotify API credentials
SPOTIPY_CLIENT_ID = 'your-spotify-client-id'
SPOTIPY_CLIENT_SECRET = 'your-spotify-client-secret'
SPOTIPY_REDIRECT_URI = 'your-app-redirect-url'

# Set up Spotify OAuth
scope = 'user-read-playback-state,user-modify-playback-state,user-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

class SpotifyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.song_input = TextInput(hint_text='Enter song name')
        self.artist_input = TextInput(hint_text='Enter artist name')
        play_button = Button(text='Play')
        play_button.bind(on_press=self.play_song)
        layout.add_widget(self.song_input)
        layout.add_widget(self.artist_input)
        layout.add_widget(play_button)
        self.status_label = Label(text='')
        layout.add_widget(self.status_label)
        return layout

    def play_song(self, instance):
        song_name = self.song_input.text
        artist_name = self.artist_input.text
        results = sp.search(q=f'{song_name} {artist_name}', type='track')
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            try:
                sp.start_playback(uris=[track_uri])
                self.status_label.text = f'Playing {song_name} by {artist_name}'
            except spotipy.exceptions.SpotifyException as e:
                self.status_label.text = f'Error playing song: {e}'
        else:
            self.status_label.text = f'Song not found: {song_name} by {artist_name}'

if __name__ == '__main__':
    SpotifyApp().run()