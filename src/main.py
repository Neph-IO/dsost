import sys
import json
import random
import os
import gi
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from ui import AudioPlayerUI  # Import UI from ui.py

# Import GStreamer with GObject Introspection
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, GLib

# Initialize GStreamer
Gst.init(None)

class AudioPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Déterminer le chemin de base en fonction de l'environnement
        if "FLATPAK_SANDBOX_DIR" in os.environ:
            # Environnement Flatpak : utiliser /app
            base_path = "/app"
        else:
            # Environnement local : remonter d'un dossier par rapport à ce script
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Définir les chemins vers les ressources en utilisant base_path
        self.data_path = os.path.join(base_path, "data")
        json_file = os.path.join(self.data_path, "playlists.json")
        version_file = os.path.join(self.data_path, "VERSION")

        # Initialize GStreamer pipeline
        self.player = Gst.ElementFactory.make("playbin", "player")
        if not self.player:
            raise Exception("GStreamer 'playbin' element could not be created. Make sure GStreamer is installed.")

        # Load playlists from JSON
        self.playlists = self.load_playlists(json_file)
        self.current_playlist = None  # Playlist currently selected

        # Read version from VERSION file
        self.version = self.read_version(version_file)

        # Set up the user interface
        AudioPlayerUI(self)  # Instantiate the user interface

        # Connect to GStreamer bus to handle buffering and state changes
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

    def read_version(self, version_file):
        try:
            with open(version_file, "r") as file:
                return file.readline().strip()
        except FileNotFoundError:
            print("VERSION file not found. Using default version.")
            return "NO VER FILE"

    def load_playlists(self, json_file):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                return data['playlists']
        except Exception as e:
            print(f"Error loading playlists: {e}")
            return []

    def select_playlist(self):
        index = self.playlist_selector.currentIndex()
        if index >= 0 and index < len(self.playlists):
            self.current_playlist = self.playlists[index]
            self.stop_player()
            self.play_pause_button.setText("▶")
            self.np_label.setText(f"Now Playing: {self.current_playlist['name']}")
            print(f"Selected playlist: {self.current_playlist['name']}")

    def toggle_play_pause(self):
        # Vérifier l'état actuel du pipeline
        state = self.player.get_state(Gst.CLOCK_TIME_NONE).state
        if state == Gst.State.PLAYING:
            # Si en cours de lecture, passer en pause
            self.player.set_state(Gst.State.PAUSED)
            self.play_pause_button.setText("▶")
        elif state == Gst.State.PAUSED:
            # Si en pause, reprendre la lecture
            self.player.set_state(Gst.State.PLAYING)
            self.play_pause_button.setText("⏸")
        elif state in (Gst.State.NULL, Gst.State.READY):
            # Si en état initial, jouer une nouvelle chanson
            self.play_random_song()

    def play_random_song(self):
        if not self.current_playlist:
            print("No playlist selected.")
            return

        # Sélectionner une piste aléatoire de la playlist
        random_index = random.randint(0, len(self.current_playlist['urls']) - 1)
        random_url = self.current_playlist['urls'][random_index]

        # Arrêter la lecture en cours en passant à l'état NULL
        self.player.set_state(Gst.State.NULL)

        # Définir l'URI sur le lecteur GStreamer
        self.player.set_property("uri", random_url)

        # Mettre à jour l'affichage du titre de la piste
        track_title = os.path.basename(random_url).split('?')[0].replace('_', ' ').replace('%20', ' ').replace('.mp3', '').replace('.flac', '').replace('.wav', '').replace('.aac', '').replace('.ogg', '')
        self.np_label.setText(f"Now Playing: {track_title}")

        # Passer à l'état PLAYING
        ret = self.player.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            print("Erreur : Impossible de démarrer la lecture.")
        else:
            print(f"Lecture de {track_title} commencée.")

    def on_message(self, bus, message):
        """Handle messages from the GStreamer bus to manage buffering and play/pause button states."""
        msg_type = message.type

        if msg_type == Gst.MessageType.BUFFERING:
            buffering_percent = message.parse_buffering()
            print(f"Buffering: {buffering_percent}%")
            if buffering_percent < 100:
                self.play_pause_button.setText("...")
                self.player.set_state(Gst.State.PAUSED)
            else:
                self.player.set_state(Gst.State.PLAYING)
                self.play_pause_button.setText("⏸")
        elif msg_type == Gst.MessageType.EOS:
            # End of Stream
            print("End of Stream going to next one")
            self.player.set_state(Gst.State.NULL)
            self.play_pause_button.setText("▶")
            self.play_random_song()
        elif msg_type == Gst.MessageType.ERROR:
            # Handle errors
            err, debug = message.parse_error()
            print(f"Error: {err}, Debug info: {debug}")
            self.player.set_state(Gst.State.NULL)
            self.play_pause_button.setText("▶")

    def set_volume(self, value):
        """Set the volume of playback."""
        self.player.set_property('volume', value / 100.0)
        print(f"Volume set to {value}%")

    def stop_player(self):
        """Stop the player."""
        self.player.set_state(Gst.State.NULL)

    def closeEvent(self, event):
        """Ensure to stop any active playback before closing."""
        print("Application closing, stopping any active playback...")
        self.stop_player()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = AudioPlayer()
    player.show()

    sys.exit(app.exec_())
