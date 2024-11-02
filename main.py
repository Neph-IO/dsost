import sys
import json
import vlc
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
import random
from ui import AudioPlayerUI  # Import UI depuis ui.py

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
        AudioPlayerUI(self)  # Instancier l'interface utilisateur
    
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
                data = json.load(f)  # Charger le JSON
                return data['playlists']  # Return the playlists
        except Exception as e:
            print(f"Erreur lors du chargement des playlists : {e}")
            return []

    def select_playlist(self):
        index = self.playlist_selector.currentIndex()
        if index >= 0 and index < len(self.playlists):
            self.current_playlist = self.playlists[index]
            self.player.stop()
            self.np_label.setText(f"Now Playing: {self.current_playlist['name']}")
            print(f"Playlist sélectionnée : {self.current_playlist['name']}")

    def toggle_play_pause(self):
        if self.player.is_playing():
            self.player.pause()
            self.play_pause_button.setText("Play")
        else:
            if self.player.get_state() == vlc.State.Paused:
                self.player.play()
                self.play_pause_button.setText("Pause")
            else:
                self.play_random_song()

            self.check_buffering()
    
    def play_random_song(self):
        if not self.current_playlist:
            print("No playlist selected.")
            return

        random_index = random.randint(0, len(self.current_playlist['urls']) - 1)
        random_url = self.current_playlist['urls'][random_index]
        
        media = self.instance.media_new(random_url)
        self.player.set_media(media)
        self.player.play()
        self.np_label.setText(f"Now Playing: {self.current_playlist['name']} - Track {random_index + 1}")
        
        self.check_buffering()

    def check_buffering(self):
        def update_state():
            print(self.player.get_state())
            if self.player.get_state() in (vlc.State.Buffering, vlc.State.Opening):
                self.play_pause_button.setText("Buffering")
            elif self.player.is_playing():
                self.play_pause_button.setText("Pause")
            else:
                self.play_pause_button.setText("Play")
                
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
