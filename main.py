import sys
from PySide6.QtWidgets import QApplication
from window import BoidsWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    window_width = 800
    window_height = 600
    SCREEN_HEIGHT = window_height
    SCREEN_WIDTH = window_width
    
    # screen = app.primaryScreen()
    # size = screen.size()
    # window_width = size.width()
    # window_height = size.height()
    # SCREEN_HEIGHT = window_height
    # SCREEN_WIDTH = window_width

    window = BoidsWindow()
    window.show()

    sys.exit(app.exec_())