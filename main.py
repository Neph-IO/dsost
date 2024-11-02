import sys
import json
import vlc
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
import random
import os
from ui import AudioPlayerUI  # Import UI from ui.py

class AudioPlayer(QMainWindow):
    def __init__(self, json_file):
        super().__init__()
        
        # Initialize VLC
        self.instance = vlc.Instance('--network-caching=500')  # Use VLC caching
        self.player = self.instance.media_player_new()
        
        # Load playlists from JSON
        self.playlists = self.load_playlists(json_file)
        self.current_playlist = None  # Playlist currently selected
        
        # Read version from VERSION file
        self.version = self.read_version()
        
        # Set up the user interface
        AudioPlayerUI(self)  # Instantiate the user interface
    
    def read_version(self):
        try:
            with open("VERSION", "r") as file:
                return file.readline().strip()
        except FileNotFoundError:
            print("VERSION file not found. Using default version.")
            return "NO VER FILE"
        
    def load_playlists(self, json_file):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)  # Load JSON data
                return data['playlists']  # Return the playlists
        except Exception as e:
            print(f"Error loading playlists: {e}")
            return []

    def select_playlist(self):
        index = self.playlist_selector.currentIndex()
        if index >= 0 and index < len(self.playlists):
            self.current_playlist = self.playlists[index]
            self.player.stop()
            self.np_label.setText(f"Now Playing: {self.current_playlist['name']}")
            print(f"Selected playlist: {self.current_playlist['name']}")

    def toggle_play_pause(self):
        if self.player.is_playing():
            self.player.pause()
            self.play_pause_button.setText("▶")
        else:
            if self.player.get_state() == vlc.State.Paused:
                self.player.play()
                self.play_pause_button.setText("⏸")
            else:
                self.play_random_song()

            self.check_buffering()
    
    def play_random_song(self):
        if not self.current_playlist:
            print("No playlist selected.")
            return

        # Select a random track from the playlist
        random_index = random.randint(0, len(self.current_playlist['urls']) - 1)
        random_url = self.current_playlist['urls'][random_index]
        
        # Load the media and start playing
        media = self.instance.media_new(random_url)
        media.parse()  # Retrieve media metadata
        self.player.set_media(media)
        self.player.play()

        # Get the title from media metadata
        track_title = media.get_meta(vlc.Meta.Title)
        if not track_title:  # If no metadata title is found, use the filename as fallback
            track_title = os.path.basename(random_url)

        # Update the display with the track title
        self.np_label.setText(f"Now Playing: {track_title}")
        
        # Check buffering state
        self.check_buffering()

    def check_buffering(self):
        def update_state():
            print(self.player.get_state())
            if self.player.get_state() in (vlc.State.Buffering, vlc.State.Opening):
                self.play_pause_button.setText("Buffering")
            elif self.player.is_playing():
                self.play_pause_button.setText("⏸")
            else:
                self.play_pause_button.setText("▶")
                
        timer = QTimer(self)
        timer.timeout.connect(update_state)
        timer.start(1000)

    def set_volume(self, value):
        self.player.audio_set_volume(value)

if __name__ == '__main__':
    json_file = 'playlists.json'
    
    app = QApplication(sys.argv)
    player = AudioPlayer(json_file)
    player.show()
    
    sys.exit(app.exec_())
