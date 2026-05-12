import urllib
import resources_rc
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QListWidget
from PySide6.QtGui import QIcon, QPainterPath, QPixmap, QPainter, QBitmap, QBrush, QColor
from PySide6.QtCore import Qt

class SpotifyWindow(QMainWindow):
    def __init__(self, spotify_logic):
        super().__init__()
        self.spotify = spotify_logic
        self.setWindowTitle("SpotiClient - Spotify Desktop Client")
        self.setMinimumSize(500, 400)

        self.setWindowIcon(QIcon(":/icon.png"))

        # Haupt-Widget und Layout
        self.main_widget = QWidget()
        self.layout = QVBoxLayout(self.main_widget)
        # In der __init__ nach den anderen Labels:
        self.label_cover = QLabel()
        self.label_cover.setFixedSize(300, 300) # Schöne quadratische Größe
        self.label_cover.setScaledContents(True) # Bild wird auf Label-Größe skaliert
        self.label_cover.setStyleSheet("border-radius: 15px; border: 2px solid #282828;")
        self.layout.addWidget(self.label_cover, alignment=Qt.AlignCenter)

        # UI Elemente
        self.label_status = QLabel("Bereit zum Laden...")
        self.label_status.setAlignment(Qt.AlignCenter)
        
        self.list_tracks = QListWidget()
        
        self.btn_refresh = QPushButton("Aktuellen Song prüfen")
        self.btn_library = QPushButton("Lieblingssongs laden")

        # Buttons mit Funktionen verbinden
        self.btn_refresh.clicked.connect(self.update_current_status)
        self.btn_library.clicked.connect(self.load_library)

        # Elemente zum Layout hinzufügen
        self.layout.addWidget(self.label_status)
        self.layout.addWidget(self.list_tracks)
        self.layout.addWidget(self.btn_refresh)
        self.layout.addWidget(self.btn_library)


        self.setCentralWidget(self.main_widget)


    def update_current_status(self):
       info = self.spotify.get_current_track_info()

       if info and info["cover"]:
           try:
               # 1. Bilddaten laden
               data = urllib.request.urlopen(info["cover"]).read()
               original_pixmap = QPixmap()
               original_pixmap.loadFromData(data)

               # 2. Ein leeres, transparentes Ziel-Pixmap erstellen
               size = self.label_cover.size()
               rounded_pixmap = QPixmap(size)
               rounded_pixmap.fill(Qt.transparent)

               # 3. Mit QPainter das Bild abgerundet zeichnen
               painter = QPainter(rounded_pixmap)
               painter.setRenderHint(QPainter.Antialiasing)
               painter.setRenderHint(QPainter.SmoothPixmapTransform)

               # Pfad für die abgerundeten Ecken (Radius hier: 30)
               path = QPainterPath()
               path.addRoundedRect(0, 0, size.width(), size.height(), 15, 15)
               painter.setClipPath(path)

               # Das Originalbild in das abgerundete Rechteck zeichnen
               painter.drawPixmap(0, 0, size.width(), size.height(), original_pixmap)
               painter.end()

               # 4. Das fertige Bild dem Label zuweisen
               self.label_status.setText(info["name"])
               self.label_cover.setPixmap(rounded_pixmap)

           except Exception as e:
               print(f"Fehler beim Abrunden: {e}")

    def load_library(self):
        self.list_tracks.clear()
        tracks = self.spotify.get_saved_tracks()
        if tracks:
            self.list_tracks.addItems(tracks)
        else:
            self.label_status.setText("Library konnte nicht geladen werden.")

    def reload_styles(self):
        try:
            with open("style.qss", "r") as f:
                from PySide6.QtWidgets import QApplication
                QApplication.instance().setStyleSheet(f.read())
            print("Styles neu geladen!")
        except Exception as e:
            print(f"Fehler beim Laden: {e}")