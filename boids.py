import sys
import random
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QSlider, QLabel, QVBoxLayout, QWidget, QPushButton
import math

# Define the parameters for the boids simulation
NUM_BOIDS = 200
BOID_SIZE = 5.0
BOID_SPEED = 5
BOID_COLOR = QColor(250, 240, 240)
#Variables PySide will control 0.0-1.0 Tunable
AVOID_FACTOR = 0.05   # Increase to encourage more avoidance
MATCHING_FACTOR = 0.05   # Increase to encourage more alignment
CENTERING_FACTOR = 0.0005   # Increase to encourage more cohesion
TURN_FACTOR = 0.2   # Reduce to make turns less aggressive
MAX_SPEED = 3.0   # Reduce to limit maximum speed
MIN_SPEED = 1.0
VIEWING_DISTANCE = 3.0  # Adjust to control the neighborhood size
PROTECTED_RANGE = 2.0   # Increase to encourage more collision avoidance
MAXBIAS = 0.01
BIAS_INCREMENT = 0.000004
BIAS_GROUPS = ["LEFT","RIGHT"]
BIAS_VAL = 0.001

# Class for an individual boid
# right now comparing every boid to every boid n*n Time complexity
class Boid:
    def __init__(self, x, y,group):
        self.x = x
        self.y = y
        self.biasGroup = group
        self.dx = random.uniform(MIN_SPEED, MAX_SPEED)  # x velocity
        self.dy = random.uniform(MIN_SPEED, MAX_SPEED)  # y velocity
        self.neighboring_boids = 0
        self.close_dx = self.close_dy = 0.0
        self.xvel_avg = self.yvel_avg = 0.0
        self.xpos_avg = self.ypos_avg = 0.0
        self.biasval = BIAS_VAL
    #Each bird attempts to maintain a reasonable amount of distance between itself and any nearby birds, to prevent overcrowding.
    def separation(self):
        self.dx += self.close_dx * AVOID_FACTOR
        self.dy += self.close_dy * AVOID_FACTOR
        return self.dx,self.dy

    #Birds try to change their position so that it corresponds with the average alignment of other nearby birds.
    def alignment(self):
        if (self.neighboring_boids > 0):
            self.xvel_avg = self.xvel_avg/self.neighboring_boids
            self.yvel_avg = self.yvel_avg/self.neighboring_boids
        self.dx += (self.xvel_avg - self.dx)*MATCHING_FACTOR
        self.dy += (self.yvel_avg - self.dy)*MATCHING_FACTOR
        return self.dx,self.dy
    
    #Every bird attempts to move towards the average position of other nearby birds.
    def cohesion(self):
        if (self.neighboring_boids > 0):
            self.xpos_avg = self.xpos_avg/self.neighboring_boids
            self.ypos_avg = self.ypos_avg/self.neighboring_boids
        self.dx += (self.xpos_avg - self.x)*CENTERING_FACTOR
        self.dy += (self.ypos_avg - self.y)*CENTERING_FACTOR
        return self.dx,self.dy


    def update(self):
        # change to collide with screen boundaries
        # FIXED: changed direction instead of location
        if self.x < 200:
            self.dx = self.dx + TURN_FACTOR
        if self.x > window_width-200:
            self.dx = self.dx - TURN_FACTOR
        if self.y < 100:
            self.dy = self.dy + TURN_FACTOR
        if self.y > window_height-100:
            self.dy = self.dy - TURN_FACTOR
            
        if (self.biasGroup =="LEFT"): 
            if (self.dx > 0):
                self.biasval = min(MAXBIAS, self.biasval + BIAS_INCREMENT)
            else:
                self.biasval = max(BIAS_INCREMENT, self.biasval - BIAS_INCREMENT)

        elif (self.biasGroup == "RIGHT"): # biased to left of screen
            if (self.dx < 0):
                self.biasval = min(MAXBIAS, self.biasval + BIAS_INCREMENT)
            else:
                self.biasval = max(BIAS_INCREMENT, self.biasval - BIAS_INCREMENT)

    # biased to right of screen
        if (self.biasGroup == "LEFT"):
            self.dx = (1 - self.biasval)*self.dx + (self.biasval * 1)
    # biased to left of screen
        elif (self.biasGroup== "RIGHT"):
            self.dx = (1 - self.biasval)*self.dx + (self.biasval * (-1))

        speed = math.sqrt(abs(self.dx*self.dx + self.dy*self.dy))
        if speed < MIN_SPEED:
            self.dx = (self.dx/speed)*MIN_SPEED
            self.dy = (self.dy/speed)*MIN_SPEED
        if speed > MAX_SPEED:
            self.dx = (self.dx/speed)*MAX_SPEED
            self.dy = (self.dy/speed)*MAX_SPEED
        self.x += self.dx
        self.y += self.dy


# Creates all boids and update boids to each other
class BoidsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.boids = [Boid(random.uniform(0, window_width), random.uniform(
            0, window_height),random.choice(BIAS_GROUPS)) for _ in range(NUM_BOIDS)]  # array of boids with different positions and speed

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_boids)
        self.timer.start(10)  # Update every 20 milliseconds

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(BOID_COLOR))

        for boid in self.boids:
            painter.drawEllipse(boid.x, boid.y, BOID_SIZE, BOID_SIZE)
# for now it is slow as every boid will be compared to every other boid in range causing n*n time complexity
# quadtree will reduce this
#such ugly nested code! will segment code into functions after
    def update_boids(self):
        for boid in self.boids:
            for otherBoid in self.boids:
                if(boid!=otherBoid):
                    dx = boid.x - otherBoid.x
                    dy = boid.y - otherBoid.y
                    if(abs(dx)<VIEWING_DISTANCE and abs(dy)<VIEWING_DISTANCE):
                        squaredDistance = dx*dx + dy*dy
                        if(squaredDistance < (PROTECTED_RANGE*PROTECTED_RANGE)):
                            boid.close_dx += boid.x - otherBoid.x
                            boid.close_dy += boid.y - otherBoid.y
                        elif (squaredDistance < (VIEWING_DISTANCE*VIEWING_DISTANCE)):
                            boid.xvel_avg += otherBoid.dx
                            boid.yvel_avg += otherBoid.dy
                            boid.xpos_avg += otherBoid.x
                            boid.ypos_avg += otherBoid.y
                            boid.neighboring_boids += 1
            if(boid.neighboring_boids>0):
                alignment = boid.alignment()
                cohesion = boid.cohesion()
                separation = boid.separation()
                boid.dx = alignment[0] + cohesion[0] + separation [0]
                boid.dy = alignment[0] + cohesion[0] + separation[0]
            boid.update()
        self.update()

class BoidsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Boids Simulation")
        self.setGeometry(0, 0, 800, 600)

        # Create the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout()

        # Create sliders and labels
        slider_layout = QHBoxLayout()

        self.avoid_slider, avoid_label = self.create_slider("Avoid Factor", AVOID_FACTOR)
        self.centering_slider, centering_label = self.create_sliderCentering("Centering Factor", CENTERING_FACTOR)
        self.matching_slider, matching_label = self.create_slider("Matching Factor", MATCHING_FACTOR)

        slider_layout.addWidget(avoid_label)
        slider_layout.addWidget(self.avoid_slider)
        slider_layout.addWidget(centering_label)
        slider_layout.addWidget(self.centering_slider)
        slider_layout.addWidget(matching_label)
        slider_layout.addWidget(self.matching_slider)

        layout.addLayout(slider_layout)

        # Create a container widget for the BoidsWidget
        boids_container = QWidget()
        boids_layout = QVBoxLayout()
        self.boids_widget = BoidsWidget()
        boids_layout.addWidget(self.boids_widget)
        boids_container.setLayout(boids_layout)

        # Add the layouts to the central widget
        layout.addWidget(boids_container)
        central_widget.setLayout(layout)

    def create_slider(self, label_text, initial_value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(1, 10)
        slider.setValue(int(initial_value * 100))
        slider.valueChanged.connect(self.slider_value_changed)

        label = QLabel(label_text)

        return slider, label
    def create_sliderCentering(self, label_text, initial_value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(1, 10)
        slider.setValue(int(initial_value * 10000))
        slider.valueChanged.connect(self.slider_value_changed)

        label = QLabel(label_text)

        return slider, label

    def slider_value_changed(self):
        # Update the variables based on the slider values
        global AVOID_FACTOR
        global CENTERING_FACTOR
        global MATCHING_FACTOR
        AVOID_FACTOR = self.avoid_slider.value() / 100.0
        CENTERING_FACTOR = self.centering_slider.value() / 100.0
        MATCHING_FACTOR = self.matching_slider.value() / 10000.0

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window_width = 800
    window_height = 600

    window = BoidsWindow()
    window.show()

    sys.exit(app.exec_())
