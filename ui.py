# ui.py
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QPushButton, QSlider
from PyQt5.QtCore import Qt

class AudioPlayerUI:
    def __init__(self, main_window):
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.main_window.setWindowTitle("Dark Souls OST player")
        self.main_window.setGeometry(100, 100, 400, 200)
        self.main_window.setFixedSize(400, 200)

        # Create a dropdown for playlists
        self.main_window.playlist_selector = QComboBox(self.main_window)
        for playlist in self.main_window.playlists:
            self.main_window.playlist_selector.addItem(playlist['name'], playlist['urls'])
        self.main_window.playlist_selector.currentIndexChanged.connect(self.main_window.select_playlist)

        # Create Play/Pause button
        self.main_window.play_pause_button = QPushButton("Play", self.main_window)
        self.main_window.play_pause_button.setFixedSize(60, 30)
        self.main_window.play_pause_button.clicked.connect(self.main_window.toggle_play_pause)

        # Create Random button
        self.main_window.random_play_button = QPushButton("Random", self.main_window)
        self.main_window.random_play_button.setFixedSize(60, 30)
        self.main_window.random_play_button.clicked.connect(self.main_window.play_random_song)

        # Volume slider
        self.main_window.volume_slider = QSlider(Qt.Horizontal, self.main_window)
        self.main_window.volume_slider.setRange(0, 100)
        self.main_window.volume_slider.setValue(80)
        self.main_window.volume_slider.valueChanged.connect(self.main_window.set_volume)
        self.main_window.player.audio_set_volume(80)

        # Labels
        self.main_window.volume_label = QLabel("Volume:", self.main_window)
        self.main_window.np_label = QLabel("Now Playing:", self.main_window)
        version_label = QLabel(self.main_window.version, self.main_window)
        version_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        version_label.setStyleSheet("font-size: 10px; color: gray;")

        # Layouts
        version_layout = QHBoxLayout()
        version_layout.addStretch()
        version_layout.addWidget(version_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.main_window.play_pause_button)
        button_layout.addWidget(self.main_window.random_play_button)
        button_layout.setAlignment(Qt.AlignLeft)

        layout = QVBoxLayout()
        layout.addWidget(self.main_window.playlist_selector)
        layout.addLayout(button_layout)
        layout.addWidget(self.main_window.np_label)
        layout.addWidget(self.main_window.volume_label)
        layout.addWidget(self.main_window.volume_slider)
        layout.addLayout(version_layout)

        # Main widget and layout
        container = QWidget()
        container.setLayout(layout)
        self.main_window.setCentralWidget(container)
        
        # Set default playlist
        self.main_window.playlist_selector.setCurrentIndex(0)
        self.main_window.select_playlist()
