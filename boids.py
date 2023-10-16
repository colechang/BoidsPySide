import sys
import random
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QBrush
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QSlider, QLabel, QVBoxLayout
import math

# Define the parameters for the boids simulation
NUM_BOIDS = 300
BOID_SIZE = 5
BOID_COLOR = QColor(250, 240, 240)

# Tunable parameters (0.0 - 1.0)
AVOID_FACTOR = 0.05     # Increase to encourage more avoidance
MATCHING_FACTOR = 0.05  # Increase to encourage more alignment
CENTERING_FACTOR = 0.0005  # Increase to encourage more cohesion
TURN_FACTOR = 0.2  # Reduce to make turns less aggressive
MAX_SPEED = 6.0  # Reduce to limit maximum speed
MIN_SPEED = 3.0  # Minimum speed

# Viewing and collision avoidance distances
VIEWING_DISTANCE = 40.0
PROTECTED_RANGE = 8.0

# Boid bias parameters
MAX_BIAS = 0.01
BIAS_INCREMENT = 0.0000004
BIAS_GROUPS = ["LEFT", "RIGHT"]
BIAS_VAL = 0.009

# Screen dimensions
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0

# Class for an individual boid
class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(MIN_SPEED, MAX_SPEED)  # x velocity
        self.dy = random.uniform(MIN_SPEED, MAX_SPEED)  # y velocity

    def separation(self, close_dx, close_dy):
        # Calculate separation based on nearby boids
        separation_x = close_dx * AVOID_FACTOR
        separation_y = close_dy * AVOID_FACTOR
        return separation_x, separation_y

    def alignment(self, x_vel_avg, y_vel_avg, neighboring_boids):
        # Calculate alignment based on nearby boids
        if neighboring_boids > 0:
            x_vel_avg = x_vel_avg / neighboring_boids
            y_vel_avg = y_vel_avg / neighboring_boids
        alignment_x = (x_vel_avg - self.dx) * MATCHING_FACTOR
        alignment_y = (y_vel_avg - self.dy) * MATCHING_FACTOR
        return alignment_x, alignment_y

    def cohesion(self, x_pos_avg, y_pos_avg, neighboring_boids):
        # Calculate cohesion based on nearby boids
        if neighboring_boids > 0:
            x_pos_avg = x_pos_avg / neighboring_boids
            y_pos_avg = y_pos_avg / neighboring_boids
        cohesion_x = (x_pos_avg - self.x) * CENTERING_FACTOR
        cohesion_y = (y_pos_avg - self.y) * CENTERING_FACTOR
        return cohesion_x, cohesion_y
    # logic for predator boid
    # def tend_to_place(self):
    #     self.dx += -self.x/10000
    #     self.dy += -self.y/10000

    def update(self):
        # change to collide with screen boundaries
        # FIXED: changed direction instead of location
        if self.x < 150:
            self.dx += TURN_FACTOR
        if self.y < 100:
            self.dy += TURN_FACTOR
        if self.x > window_width-150:
            self.dx -= TURN_FACTOR
        if self.y > window_height-100:
            self.dy -= TURN_FACTOR

        """    
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
        """
        speed = math.sqrt(abs(self.dx*self.dx + self.dy*self.dy))
        if speed < MIN_SPEED:
            self.dx = (self.dx/speed)*MIN_SPEED
            self.dy = (self.dy/speed)*MIN_SPEED
        if speed > MAX_SPEED:
            self.dx = (self.dx/speed)*MAX_SPEED
            self.dy = (self.dy/speed)*MAX_SPEED
        #self.tend_to_place()
        self.x += self.dx
        self.y += self.dy


# Creates all boids and update boids to each other
class BoidsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.boids = [Boid(random.uniform(0, window_width), random.uniform(
            0, window_height)) for _ in range(NUM_BOIDS)]  # array of boids with different positions and speed
        
        """self.boids = [Boid(random.uniform(0,window_width),random.uniform(0,window_height),"PREDATOR")] + [Boid(random.uniform(0, window_width), random.uniform(
            0, window_height),random.choice(BIAS_GROUPS)) for _ in range(NUM_BOIDS)]  # array of boids with different positions and speed"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_boids)
        self.timer.start(1)  # Update every 20 milliseconds

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(BOID_COLOR))

        for boid in self.boids:
            # if boid == self.boids[0]:
            #     painter.setBrush(QBrush(QColor(255,0,0)))
            #     painter.drawEllipse(boid.x, boid.y, BOID_SIZE+3, BOID_SIZE+3)
            # else:
            painter.drawEllipse(boid.x, boid.y, BOID_SIZE, BOID_SIZE)
            
    def update_boids(self):
        for boid in self.boids:
            xvel_avg = yvel_avg = xpos_avg = ypos_avg = close_dx = close_dy = 0.0
            neighboring_boids = 0
            for otherBoid in self.boids:
                if(boid!=otherBoid): #or boid.biasGroup=="LEADER"
                    dx = boid.x - otherBoid.x
                    dy = boid.y - otherBoid.y
                    if(abs(dx)<VIEWING_DISTANCE and abs(dy)<VIEWING_DISTANCE):
                        squaredDistance = (dx*dx) + (dy*dy)
                        if(squaredDistance < (PROTECTED_RANGE*PROTECTED_RANGE)):
                            close_dx += boid.x - otherBoid.x
                            close_dy += boid.y - otherBoid.y
                        elif (squaredDistance < (VIEWING_DISTANCE*VIEWING_DISTANCE)):
                            xvel_avg += otherBoid.dx
                            yvel_avg += otherBoid.dy
                            xpos_avg += otherBoid.x
                            ypos_avg += otherBoid.y
                            neighboring_boids += 1
            separation = boid.separation(close_dx,close_dy)
            boid.dx += separation[0]
            boid.dy += separation[1]
            if(neighboring_boids>0):
                alignment = boid.alignment(xvel_avg,yvel_avg,neighboring_boids)
                cohesion = boid.cohesion(xpos_avg,ypos_avg,neighboring_boids)
                boid.dx += alignment[0] + cohesion[0] 
                boid.dy += alignment[1] + cohesion[1]
            boid.update()
        self.update()

class BoidsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Boids Simulation")
        self.setGeometry(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Create the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout()

        # Create sliders and labels
        slider_layout = QHBoxLayout()

        self.avoid_slider, avoid_label = self.create_sliderSeparation("Avoid Factor", AVOID_FACTOR)
        self.centering_slider, centering_label = self.create_sliderCentering("Centering Factor", CENTERING_FACTOR)
        self.matching_slider, matching_label = self.create_sliderMatching("Matching Factor", MATCHING_FACTOR)
        self.max_speed_slider, max_speed_label = self.create_sliderMaxSpeed("Max Speed", MAX_SPEED)
        self.min_speed_slider,min_speed_slider = self.create_sliderMaxSpeed("Min Speed", MIN_SPEED)
        slider_layout.addWidget(self.max_speed_slider)
        slider_layout.addWidget(max_speed_label)
        slider_layout.addWidget(self.min_speed_slider)
        slider_layout.addWidget(min_speed_slider)
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

    def create_sliderMaxSpeed(self,label_text,initial_value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(5,20)
        slider.setValue(int(initial_value))
        slider.valueChanged.connect(self.slider_value_changed)
        
        label = QLabel(label_text)
        
        return slider,label


    def create_sliderMinSpeed(self,label_text,initial_value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0,4)
        slider.setValue(int(initial_value))
        slider.valueChanged.connect(self.slider_value_changed)
        
        label = QLabel(label_text)
        
        return slider,label

    def create_sliderSeparation(self, label_text, initial_value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(1, 100)
        slider.setValue(int(initial_value * 100))
        slider.valueChanged.connect(self.slider_value_changed)

        label = QLabel(label_text)

        return slider, label
    def create_sliderCentering(self, label_text, initial_value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(1, 100)
        slider.setValue(int(initial_value * 10000))
        slider.valueChanged.connect(self.slider_value_changed)

        label = QLabel(label_text)

        return slider, label
    def create_sliderMatching(self, label_text, initial_value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(1, 100)
        slider.setValue(int(initial_value * 100))
        slider.valueChanged.connect(self.slider_value_changed)

        label = QLabel(label_text)

        return slider, label
    def slider_value_changed(self):
        # Update the variables based on the slider values
        global AVOID_FACTOR
        global CENTERING_FACTOR
        global MATCHING_FACTOR
        AVOID_FACTOR = self.avoid_slider.value() / 100.0
        CENTERING_FACTOR = self.centering_slider.value() / 10000.0
        MATCHING_FACTOR = self.matching_slider.value() / 100.0
    
    def speed_slider_value_changed(self):
        global MAX_SPEED
        global MIN_SPEED
        MAX_SPEED = self.max_speed_slider.value()
        MIN_SPEED = self.min_speed_slider.value()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    window_width = 800
    window_height = 600
    SCREEN_HEIGHT = window_height
    SCREEN_WIDTH = window_width

    window = BoidsWindow()
    window.show()

    sys.exit(app.exec_())