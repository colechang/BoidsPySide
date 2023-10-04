import sys
import random
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
import math

# Define the parameters for the boids simulation
NUM_BOIDS = 50
BOID_SIZE = 10
BOID_SPEED = 5
BOID_COLOR = QColor(250, 249, 246)

# Class for an individual boid


class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(-BOID_SPEED, BOID_SPEED)  # x velocity
        self.dy = random.uniform(-BOID_SPEED, BOID_SPEED)  # y velocity
        self.angle = random.uniform(0.0, 2.0 * math.pi)
        self.viewingAngle = 4.71239  # 270 Degrees

    def seperation(self):
        close_dx = 0
        close_dy = 0
        close_dx += self.x - otherboid.x
        close_dy += self.y - otherboid.y
        self.vx += close_dx * avoidfactor
        self.vy += close_dy * avoidfactor

    def update(self):
        # Update the boid's position
        self.x += self.dx
        self.y += self.dy

        # change to collide with screen boundaries
        # FIXED: changed direction instead of location
        if self.x < 0:
            self.dx = -self.dx
        elif self.x > window_width:
            self.dx = -self.dx

        if self.y < 0:
            self.dy = -self.dy
        elif self.y > window_height:
            self.dy = -self.dy
# Creates all boids and update boids to each other


class BoidsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.boids = [Boid(random.uniform(0, window_width), random.uniform(
            0, window_height)) for _ in range(NUM_BOIDS)]

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_boids)
        self.timer.start(10)  # Update every 20 milliseconds

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(BOID_COLOR))

        for boid in self.boids:
            painter.drawEllipse(boid.x, boid.y, BOID_SIZE, BOID_SIZE)

    def update_boids(self):
        for boid in self.boids:
            boid.update()

        self.update()


class BoidsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Boids Simulation")
        self.setGeometry(100, 100, 800, 800)

        central_widget = BoidsWidget()
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window_width = 800
    window_height = 800

    window = BoidsWindow()
    window.show()

    sys.exit(app.exec_())
