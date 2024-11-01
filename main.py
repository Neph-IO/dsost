import sys
import json
import vlc
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QSlider, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox
from PyQt5.QtCore import Qt, QTimer
import random

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
        self.init_ui()
    
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

    def init_ui(self):
        version = "0.1.1"
        # Set window properties
        self.setWindowTitle("Dark Souls OST player")
        self.setGeometry(100, 100, 400, 200)
        self.setFixedSize(400, 200)
        
        # Create a dropdown for playlists
        self.playlist_selector = QComboBox(self)
        for playlist in self.playlists:
            self.playlist_selector.addItem(playlist['name'], playlist['urls'])  # Ajouter le nom de la playlist et ses URLs
        
        self.playlist_selector.currentIndexChanged.connect(self.select_playlist)

        # Create the Play/Pause button with fixed size
        self.play_pause_button = QPushButton("Play", self)
        self.play_pause_button.setFixedSize(60, 30)  # Set button size to ~1 cm
        self.play_pause_button.clicked.connect(self.toggle_play_pause)

        # Create Next random button with fixed size
        self.random_play_button = QPushButton("Random", self)
        self.random_play_button.setFixedSize(60, 30)   # Set button size to ~1 cm
        self.random_play_button.clicked.connect(self.play_random_song)
            
        # Create the volume slider
        self.volume_slider = QSlider(Qt.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)  # Default volume level
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.player.audio_set_volume(80)  # Set initial VLC player volume
        
        # Volume label
        self.volume_label = QLabel("Volume:", self)

        # NowPlaying label
        self.np_label = QLabel("Now Playing:", self)

        # Add a small label for the version number in the bottom right
        version_label = QLabel(self.version, self)
        version_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        version_label.setStyleSheet("font-size: 10px; color: gray;")  # Small font, subtle color

        # Create a layout for version label
        version_layout = QHBoxLayout()
        version_layout.addStretch()  # Push label to the right
        version_layout.addWidget(version_label)

        # Set horizontal Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_pause_button)
        button_layout.addWidget(self.random_play_button)
        button_layout.setAlignment(Qt.AlignLeft)  # Align buttons to the left side

        # Set Vertical layout
        layout = QVBoxLayout()
        layout.addWidget(self.playlist_selector)
        layout.addLayout(button_layout)
        layout.addWidget(self.np_label)
        layout.addWidget(self.volume_label)
        layout.addWidget(self.volume_slider)
        layout.addLayout(version_layout)
        
        # Set the main widget and layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Select the first playlist by default
        self.playlist_selector.setCurrentIndex(0)  # Select the first playlist
        self.select_playlist()  # Load the first playlist immediately

    def select_playlist(self):
        # Get the selected playlist and URLs
        index = self.playlist_selector.currentIndex()
        if index >= 0 and index < len(self.playlists):
            self.current_playlist = self.playlists[index]
            self.player.stop()
            self.np_label.setText(f"Now Playing: {self.current_playlist['name']}")  # Display selected playlist
            print(f"Playlist sélectionnée : {self.current_playlist['name']}")  # Debug

    def toggle_play_pause(self):
        # If the player is currently playing, pause it
        if self.player.is_playing():
            self.player.pause()
            self.play_pause_button.setText("Play")
        else:
            # If the player is paused, resume playback without reloading the song
            if self.player.get_state() == vlc.State.Paused:
                self.player.play()
                self.play_pause_button.setText("Pause")
            else:
                self.play_random_song()

            # Check buffering state
            self.check_buffering()
    
    def play_random_song(self):
        if not self.current_playlist:
            print("No playlist selected.")  # Debug
            return

        # Choose a random song from the current playlist
        random_index = random.randint(0, len(self.current_playlist['urls']) - 1)
        random_url = self.current_playlist['urls'][random_index]
        
        # Load and play the random song
        media = self.instance.media_new(random_url)
        self.player.set_media(media)
        self.player.play()
        self.np_label.setText(f"Now Playing: {self.current_playlist['name']} - Track {random_index + 1}")
        
        # Check buffering state
        self.check_buffering()

    def check_buffering(self):
        # Create a timer to check the state
        def update_state():
            print(self.player.get_state())  # Debug
            if self.player.get_state() in (vlc.State.Buffering, vlc.State.Opening):
                self.play_pause_button.setText("Buffering")
            elif self.player.is_playing():
                self.play_pause_button.setText("Pause")
            else:
                self.play_pause_button.setText("Play")
                

        # Use a QTimer to periodically check the state
        timer = QTimer(self)
        timer.timeout.connect(update_state)
        timer.start(1000)  # Check every second

    def set_volume(self, value):
        # Set VLC player volume
        self.player.audio_set_volume(value)

# Main execution
if __name__ == '__main__':
    json_file = 'playlists.json'  # Remplace par le chemin de ton fichier JSON
    
    # Create the application
    app = QApplication(sys.argv)
    
    # Create and show the audio player window
    player = AudioPlayer(json_file)
    player.show()
    
    # Start the application event loop
    sys.exit(app.exec_())
