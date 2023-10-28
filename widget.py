# Creates all boids and update boids to each other
from quadtree import Quadtree
from quadtree import Boundary
from boid import Boid
from boid import random
import time
import os
import psutil
from constants import NUM_BOIDS, BOID_SIZE, PROTECTED_RANGE,VIEWING_DISTANCE,INTERPOLATION_ALPHA
from boid import *
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtWidgets import QWidget 
from PySide6.QtCore import QTimer

BOID_COLOR = QColor(255, 255, 255)


class BoidsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.boundary = Boundary(0, 0,SCREEN_WIDTH, SCREEN_HEIGHT)
        self.quadtree = Quadtree(self.boundary, 16)  # Adjust the capacity as needed
        self.boids = [Boid(random.uniform(0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT)) for _ in range(NUM_BOIDS)]
        for boid in self.boids:
            self.quadtree.insert(boid)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_boids)
        self.timer.start(32)

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(BOID_COLOR))

        for boid in self.boids:
            painter.drawEllipse(boid.x, boid.y, BOID_SIZE, BOID_SIZE)
    
    def update_boids(self):
        start_time = time.time()
        
        self.quadtree.clear()
        for boid in self.boids:
            search_boundary = Boundary(boid.x, boid.y, VIEWING_DISTANCE*2, VIEWING_DISTANCE*2)
            neighboring_boids = self.quadtree.query(search_boundary)
            xvel_avg = yvel_avg = xpos_avg = ypos_avg = close_dx = close_dy = 0.0
            for otherBoid in neighboring_boids:
                if(boid!=otherBoid):
                    dx = boid.x - otherBoid.x
                    dy = boid.y - otherBoid.y
                    #alter viewing distance and protected range values and checks if withing boundary instead
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
            separation = boid.separation(close_dx,close_dy)
            boid.dx += separation[0]
            boid.dy += separation[1]
            if(len(neighboring_boids)>0):
                alignment = boid.alignment(xvel_avg,yvel_avg,len(neighboring_boids))
                cohesion = boid.cohesion(xpos_avg,ypos_avg,len(neighboring_boids))
                boid.dx += alignment[0] + cohesion[0] 
                boid.dy += alignment[1] + cohesion[1]
            new_x = boid.x + boid.dx
            new_y = boid.y + boid.dy
            boid.lerp(new_x, new_y, INTERPOLATION_ALPHA) 
            boid.update()
            load1, load5, load15 = psutil.getloadavg()
        
            cpu_usage = (load15/os.cpu_count()) * 100
            
            print("The CPU usage is : ", cpu_usage)
        self.update()
        time_now = time.time()
        print("FPS: ", 1.0 / (time_now - start_time))
