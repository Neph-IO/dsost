from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QPushButton, QSlider, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

class AudioPlayerUI:
    def __init__(self, main_window):
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.main_window.setWindowTitle("Dark Souls OST player")
        self.main_window.setGeometry(100, 100, 400, 100)
        self.main_window.setFixedSize(400, 100)
        
        # Create Play/Pause button with ASCII icons
        self.main_window.play_pause_button = QPushButton("▶", self.main_window)  # Start with play symbol
        self.main_window.play_pause_button.setFixedSize(30, 30)
        self.main_window.play_pause_button.clicked.connect(self.main_window.toggle_play_pause)

        # Create Random button with the ↺ symbol
        self.main_window.random_play_button = QPushButton("↺", self.main_window)  # Using the rotation symbol for random play
        self.main_window.random_play_button.setFixedSize(30, 30)
        self.main_window.random_play_button.clicked.connect(self.main_window.play_random_song)

        # Create a dropdown for playlists
        self.main_window.playlist_selector = QComboBox(self.main_window)
        for playlist in self.main_window.playlists:
            self.main_window.playlist_selector.addItem(playlist['name'], playlist['urls'])
        self.main_window.playlist_selector.currentIndexChanged.connect(self.main_window.select_playlist)

        # Volume slider (vertical)
        self.main_window.volume_slider = QSlider(Qt.Vertical, self.main_window)
        self.main_window.volume_slider.setRange(0, 100)
        self.main_window.volume_slider.setValue(80)
        self.main_window.volume_slider.valueChanged.connect(self.main_window.set_volume)
        self.main_window.player.audio_set_volume(80)

        # Labels
        self.main_window.np_label = QLabel("Now Playing:", self.main_window)
        version_label = QLabel(self.main_window.version, self.main_window)
        version_label.setAlignment(Qt.AlignRight)
        version_label.setStyleSheet("font-size: 10px; color: gray;")

        # Layout for the Now Playing and version labels
        now_playing_layout = QHBoxLayout()
        now_playing_layout.addWidget(self.main_window.np_label)
        now_playing_layout.addStretch()
        now_playing_layout.addWidget(version_label)

        # Layout to position the buttons to the left of the playlist selector
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.main_window.play_pause_button)  # Add Play button first
        control_layout.addWidget(self.main_window.random_play_button)  # Add Random button next
        control_layout.addWidget(self.main_window.playlist_selector)  # Playlist selector to the right of the buttons

        # Top layout with control layout and volume slider aligned to the top
        top_layout = QHBoxLayout()
        top_layout.addLayout(control_layout)
        top_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        top_layout.addWidget(self.main_window.volume_slider, alignment=Qt.AlignTop)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(now_playing_layout)
        main_layout.addStretch()

        # Main widget and layout
        container = QWidget()
        container.setLayout(main_layout)
        self.main_window.setCentralWidget(container)

        # Set default playlist
        self.main_window.playlist_selector.setCurrentIndex(0)
        self.main_window.select_playlist()
