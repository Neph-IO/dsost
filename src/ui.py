from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QSlider, QSpacerItem, QSizePolicy, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsOpacityEffect
import os

class AudioPlayerUI:
    def __init__(self, main_window):
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        # Déterminer le chemin de base en fonction de l'environnement
        if "FLATPAK_SANDBOX_DIR" in os.environ:
            # Environnement Flatpak : utiliser /app
            base_path = "/app"
        else:
            # Environnement local : remonter d'un dossier par rapport à ce script
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Chemins des ressources
        data_path = os.path.join(base_path, "data")
        bg_path = os.path.join(data_path, "bg.jpg")
        icon_path = os.path.join(data_path, "dsicon.png")

        # Set window properties
        self.main_window.setWindowTitle("Dark Souls OST player")
        self.main_window.setGeometry(100, 100, 400, 100)
        self.main_window.setFixedSize(400, 100)

        # Définir l'icône de la fenêtre
        self.main_window.setWindowIcon(QIcon(icon_path))

        # Define a global stylesheet for the text color
        self.main_window.setStyleSheet("color: #ebdbb2; font-family: Arial, sans-serif;")

        # Create a QLabel for the background image
        self.background_label = QLabel(self.main_window)
        self.background_label.setGeometry(self.main_window.rect())
        self.background_pixmap = QPixmap(bg_path)
        self.background_label.setPixmap(self.background_pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.lower()  # Send the QLabel to the background

        # Set opacity for the background image
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.3)
        self.background_label.setGraphicsEffect(opacity_effect)

        # Main container for the interface elements
        main_container = QWidget(self.main_window)
        main_layout = QVBoxLayout(main_container)

        # Create Play/Pause button
        self.main_window.play_pause_button = QPushButton("▶", main_container)
        self.main_window.play_pause_button.setFixedSize(40, 40)
        self.main_window.play_pause_button.clicked.connect(self.main_window.toggle_play_pause)
        self.main_window.play_pause_button.setStyleSheet("background-color: #2b3339; color: #ebdbb2; border: 1px solid #4e796d; border-radius: 8px; padding: 8px;")

        # Create Random button
        self.main_window.random_play_button = QPushButton("↺", main_container)
        self.main_window.random_play_button.setFixedSize(40, 40)
        self.main_window.random_play_button.clicked.connect(self.main_window.play_random_song)
        self.main_window.random_play_button.setStyleSheet("background-color: #2b3339; color: #ebdbb2; border: 1px solid #4e796d; border-radius: 8px; padding: 8px;")

        # Create a dropdown for playlists
        self.main_window.playlist_selector = QComboBox(main_container)
        for playlist in self.main_window.playlists:
            self.main_window.playlist_selector.addItem(playlist['name'], playlist['urls'])
        self.main_window.playlist_selector.currentIndexChanged.connect(self.main_window.select_playlist)
        self.main_window.playlist_selector.setStyleSheet("background-color: #2b3339; color: #ebdbb2; border: 1px solid #4e796d; padding: 5px;")

        # Volume slider (vertical)
        self.main_window.volume_slider = QSlider(Qt.Vertical, main_container)
        self.main_window.volume_slider.setRange(0, 100)
        self.main_window.volume_slider.setValue(80)
        self.main_window.volume_slider.valueChanged.connect(self.main_window.set_volume)
        self.main_window.volume_slider.setStyleSheet("QSlider::groove:vertical { background: #2b3339; width: 10px; border-radius: 2px; border: 1px solid #4e796d;} QSlider::handle:vertiacal { background: #ebdbb2; border: 1px solid #2b3339; height: 20px; width: 20px; margin: -5px 0; border-radius: 10px; }")

        # Labels
        self.main_window.np_label = QLabel("Now Playing:", main_container)
        self.main_window.np_label.setStyleSheet("font-size: 14px; font-weight: bold;")

        version_label = QLabel(self.main_window.version, main_container)
        version_label.setAlignment(Qt.AlignRight)
        version_label.setStyleSheet("font-size: 10px; color: gray;")

        # Layout for the Now Playing and version labels
        now_playing_layout = QHBoxLayout()
        now_playing_layout.addWidget(self.main_window.np_label)
        now_playing_layout.addStretch()
        now_playing_layout.addWidget(version_label)

        # Layout to position the buttons to the left of the playlist selector
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.main_window.play_pause_button)
        control_layout.addWidget(self.main_window.random_play_button)
        control_layout.addWidget(self.main_window.playlist_selector)

        # Top layout with control layout and volume slider aligned to the center
        top_layout = QHBoxLayout()
        top_layout.addLayout(control_layout)
        top_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        top_layout.addWidget(self.main_window.volume_slider, alignment=Qt.AlignVCenter)

        # Main layout to organize everything
        main_layout.addLayout(top_layout)
        main_layout.addLayout(now_playing_layout)
        main_layout.addStretch()

        # Set the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.main_window.setCentralWidget(container)

        # Set default playlist
        self.main_window.playlist_selector.setCurrentIndex(0)
        self.main_window.select_playlist()
