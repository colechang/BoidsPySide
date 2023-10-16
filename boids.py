import random
from config import MIN_SPEED,MAX_SPEED,AVOID_FACTOR,MATCHING_FACTOR,CENTERING_FACTOR,TURN_FACTOR,window_height,window_width
import math

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