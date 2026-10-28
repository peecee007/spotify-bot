import os
import logging
import threading
import tkinter as tk
import speech_recognition as sr
import pyttsx3
from musickit import MusicKit
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Setup logging
logging.basicConfig(
    filename="voice_commands.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Initialize MusicKit for Apple Music
music_kit = MusicKit()

# Initialize Spotify client - fill in your credentials here
SPOTIFY_CLIENT_ID = "0e12fsZ2wpqmDsFH9nh8xUceKKyVvJdkXV4h"
SPOTIFY_CLIENT_SECRET = "b0bd586caf004e3aa82615bbde4b07f5"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"

scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
spotify_auth_manager = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                    client_secret=SPOTIFY_CLIENT_SECRET,
                                    redirect_uri=SPOTIFY_REDIRECT_URI,
                                    scope=scope)

spotify = spotipy.Spotify(auth_manager=spotify_auth_manager)

# Initialize recognizer and TTS
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def update_status(text):
    status_label.config(text=text)

def listen():
    with sr.Microphone() as source:
        update_status("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            logging.info(command)
            update_status(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            update_status("Unrecognized speech.")
        except sr.RequestError:
            speak("Speech recognition service unavailable.")
            update_status("Speech service error.")
        return ""

def play_on_spotify(song_name):
    try:
        results = spotify.search(q=song_name, limit=1, type='track')
        tracks = results.get('tracks', {}).get('items', [])
        if not tracks:
            speak("I couldn't find that song on Spotify.")
            update_status("Song not found on Spotify.")
            return
        track = tracks[0]
        uri = track['uri']

        # Get current playback device
        devices = spotify.devices()
        if not devices['devices']:
            speak("No active Spotify device found. Please open Spotify on a device.")
            update_status("No active Spotify device.")
            return
        device_id = devices['devices'][0]['id']

        spotify.start_playback(device_id=device_id, uris=[uri])
        speak(f"Playing {track['name']} by {track['artists'][0]['name']} on Spotify.")
        update_status(f"Playing on Spotify: {track['name']} - {track['artists'][0]['name']}")
    except Exception as e:
        logging.error(f"Spotify playback error: {e}")
        speak("Sorry, I couldn't play the song on Spotify.")
        update_status("Spotify playback error.")

def play_on_apple_music(song_name):
    try:
        music_kit.play_song(song_name)
        speak(f"Playing {song_name} on Apple Music.")
        update_status(f"Playing on Apple Music: {song_name}")
    except Exception as e:
        logging.error(f"Apple Music playback error: {e}")
        speak("Sorry, I couldn't play the song on Apple Music.")
        update_status("Apple Music playback error.")

def handle_command(command):
    if "play" in command:
        # Determine platform if specified
        if "spotify" in command:
            song_name = command.replace("play", "").replace("on spotify", "").strip()
            if song_name:
                play_on_spotify(song_name)
            else:
                speak("Please say the name of the song you want to play on Spotify.")
                update_status("No song name detected.")
        elif "apple music" in command:
            song_name = command.replace("play", "").replace("on apple music", "").strip()
            if song_name:
                play_on_apple_music(song_name)
            else:
                speak("Please say the name of the song you want to play on Apple Music.")
                update_status("No song name detected.")
        else:
            # Default to Apple Music
            song_name = command.replace("play", "").strip()
            if song_name:
                play_on_apple_music(song_name)
            else:
                speak("Please say the name of the song you want to play.")
                update_status("No song name detected.")
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        root.destroy()
    else:
        speak("Command not recognized.")
        update_status("Unknown command.")

def run_voice_command():
    command = listen()
    if command:
        handle_command(command)

def threaded_listen():
    threading.Thread(target=run_voice_command, daemon=True).start()

# --- GUI Setup ---
root = tk.Tk()
root.title("Voice Music Assistant")
root.geometry("450x220")

title = tk.Label(root, text="🎵 Voice Music Assistant", font=("Helvetica", 16))
title.pack(pady=10)

status_label = tk.Label(root, text="Press the button and speak", fg="blue")
status_label.pack(pady=10)

listen_button = tk.Button(root, text="🎤 Listen", command=threaded_listen, width=25, height=2)
listen_button.pack(pady=10)

quit_button = tk.Button(root, text="Exit", command=root.destroy, width=10)
quit_button.pack(pady=5)

root.mainloop()
