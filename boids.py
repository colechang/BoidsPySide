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
#Variables PySide will control 0.0-1.0 Tunable
AVOID_FACTOR = 0.5
MATCHING_FACTOR = 0.5
CENTERING_FACTOR = 0.5
TURN_FACTOR = 0.2
MAX_SPEED = 6
MIN_SPEED = 3
VIEWING_DISTANCE = 40
PROTECTED_RANGE = 5

# Class for an individual boid
# right now comparing every boid to every boid n*n Time complexity
class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(-BOID_SPEED, BOID_SPEED)  # x velocity
        self.dy = random.uniform(-BOID_SPEED, BOID_SPEED)  # y velocity
        self.neighboring_boids = 0
        self.close_dx = self.close_dy = 0
        self.xvel_avg = self.yvel_avg = 0
        self.xpos_avg = self.ypos_avg = 0
    #Each bird attempts to maintain a reasonable amount of distance between itself and any nearby birds, to prevent overcrowding.
    def separation(self,otherboid):
        self.close_dx = self.close_dy = 0
        self.close_dx += self.x - otherboid.x
        self.close_dy += self.y - otherboid.y
        self.dx += self.close_dx * AVOID_FACTOR
        self.dy += self.close_dy * AVOID_FACTOR
    #Birds try to change their position so that it corresponds with the average alignment of other nearby birds.
    def alignment(self,otherboid):
        self.xvel_avg = self.yvel_avg = 0
        self.xvel_avg += otherboid.dx
        self.yvel_avg += otherboid.dy
        self.neighboring_boids += 1
        if (self.neighboring_boids > 0):
            self.xvel_avg = self.xvel_avg/self.neighboring_boids
            self.yvel_avg = self.yvel_avg/self.neighboring_boids
        self.dx += (self.xvel_avg - self.dx)*MATCHING_FACTOR
        self.dy += (self.yvel_avg - self.dy)*MATCHING_FACTOR
    
    #Every bird attempts to move towards the average position of other nearby birds.
    def cohesion(self,otherboid):
        self.xpos_avg = self.ypos_avg = 0
        self.xpos_avg += otherboid.x
        self.ypos_avg += otherboid.y
        self.neighboring_boids += 1
        if (self.neighboring_boids > 0):
            self.xpos_avg = self.xpos_avg/self.neighboring_boids
            self.ypos_avg = self.ypos_avg/self.neighboring_boids
        self.dx += (self.xpos_avg - self.x)*CENTERING_FACTOR
        self.dy += (self.ypos_avg - self.y)*CENTERING_FACTOR

    def update(self,otherBoid):

        # # Update the boid's position
        # self.separation(otherBoid)
        # self.alignment(otherBoid)
        # self.cohesion(otherBoid)

        # change to collide with screen boundaries
        # FIXED: changed direction instead of location
        if self.x < 0:
            self.dx = self.dx + TURN_FACTOR
        if self.x > window_width:
            self.dx = self.dx - TURN_FACTOR
        if self.y < 0:
            self.dy = self.dy - TURN_FACTOR
        elif self.y > window_height:
            self.dy = self.dy + TURN_FACTOR

        speed = math.sqrt(self.dx*self.dx + self.dy*self.dy)
        if speed < MIN_SPEED:
            self.dx = (self.dx/speed)*MIN_SPEED
            self.dy = (self.dy/speed)*MIN_SPEED
        if speed > MIN_SPEED:
            self.dx = (self.dx/speed)*MAX_SPEED
            self.dy = (self.dy/speed)*MAX_SPEED
        self.x += self.dx
        self.y += self.dy


# Creates all boids and update boids to each other
class BoidsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.boids = [Boid(random.uniform(0, window_width), random.uniform(
            0, window_height)) for _ in range(NUM_BOIDS)]  # array of boids with different positions and speed

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
            for otherBoid in self.boids:
                if(boid!=otherBoid):
                    dx = boid.x - otherBoid.x
                    dy = boid.y - otherBoid.y
                    if(abs(dx)<VIEWING_DISTANCE and abs(dy)<VIEWING_DISTANCE):
                        squaredDistance = dx*dx + dy*dy
                        if(squaredDistance < (PROTECTED_RANGE*PROTECTED_RANGE)):
                            boid.separation(otherBoid)
                        elif (squaredDistance < (VIEWING_DISTANCE*VIEWING_DISTANCE)):
                            self.xpos_avg += otherBoid.x 
                            self.ypos_avg += otherBoid.y 
                            self.xvel_avg += otherBoid.dx
                            self.yvel_avg += otherBoid.dy
                            self.neighboring_boids += 1
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
