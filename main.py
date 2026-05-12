import sys
import ctypes
from PySide6.QtWidgets import QApplication
from spotify_client import SpotifyHandler
from gui import SpotifyWindow

def main():
    app = QApplication(sys.argv)

    app_id = 'piet.spoticlient.v1'

    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    app.setDesktopFileName("spoticlient")

    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Stylesheet nicht gefunden, nutze Standard-Look.")

    spotify = SpotifyHandler()
    
    window = SpotifyWindow(spotify)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()