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

    # avoid factor will be tunable
    def seperation(boid):
        close_dx = 0
        close_dy = 0
        close_dx += boid.x - otherboid.x
        close_dy += boid.y - otherboid.y
        boid.vx += close_dx * avoidfactor
        boid.vy += close_dy * avoidfactor

    # matching factor will be tunable
    def alignment(boid):
        xvel_avg, yvel_avg, neighboring_boids = 0
        xvel_avg += otherboid.vx
        yvel_avg += otherboid.vy
        neighboring_boids += 1
        if (neighboring_boids > 0):
            xvel_avg = xvel_avg/neighboring_boids
            yvel_avg = yvel_avg/neighboring_boids
        boid.dx += (xvel_avg - boid.dx)*matchingfactor
        boid.dy += (yvel_avg - boid.dy)*matchingfactor

    # centering factor will be tunable
    def cohesion(boid):
        xpos_avg, ypos_avg, neighboring_boids = 0
        xpos_avg += otherboid.x
        ypos_avg += otherboid.y
        neighboring_boids += 1
        if (neighboring_boids > 0):
            xpos_avg = xpos_avg/neighboring_boids
            ypos_avg = ypos_avg/neighboring_boids
        boid.dx += (xpos_avg - boid.x)*centeringfactor
        boid.dy += (ypos_avg - boid.y)*centeringfactor

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
            0, window_height)) for _ in range(NUM_BOIDS)]  # array of boids

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_boids)
        self.timer.start(10)  # Update every 20 milliseconds

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(BOID_COLOR))

        for boid in self.boids:
            painter.drawEllipse(boid.x, boid.y, BOID_SIZE, BOID_SIZE)
# for now it is slow as every boid will be compared to every other boid in range causing n*n time complexity
# quadtree will reduce this

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
