import sys
from PySide6.QtWidgets import QApplication
from boidswidget import BoidsWidget
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from gui import BoidsWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    global window_width
    window_width = 800
    window_height = 600
    global SCREEN_HEIGHT
    global SCREEN_WIDTH
    SCREEN_HEIGHT = window_height
    SCREEN_WIDTH = window_width

    window = BoidsWindow()
    window.show()

    sys.exit(app.exec_())
