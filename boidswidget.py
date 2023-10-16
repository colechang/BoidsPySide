from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter, QBrush
import random
from boids import Boid
from config import window_height,window_width, NUM_BOIDS, BOID_COLOR,BOID_SIZE,VIEWING_DISTANCE,PROTECTED_RANGE

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
        self.timer.start(10)  # Update every 10 milliseconds

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