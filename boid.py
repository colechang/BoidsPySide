import random
import math
from constants import SCREEN_HEIGHT,SCREEN_WIDTH,MATCHING_FACTOR,MAX_SPEED,MIN_SPEED,CENTERING_FACTOR,AVOID_FACTOR,TURN_FACTOR

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
        x_vel_avg = x_vel_avg / neighboring_boids
        y_vel_avg = y_vel_avg / neighboring_boids
        alignment_x = (x_vel_avg - self.dx) * MATCHING_FACTOR
        alignment_y = (y_vel_avg - self.dy) * MATCHING_FACTOR
        return alignment_x, alignment_y

    def cohesion(self, x_pos_avg, y_pos_avg, neighboring_boids):
        # Calculate cohesion based on nearby boids
        x_pos_avg = x_pos_avg / neighboring_boids
        y_pos_avg = y_pos_avg / neighboring_boids
        cohesion_x = (x_pos_avg - self.x) * CENTERING_FACTOR
        cohesion_y = (y_pos_avg - self.y) * CENTERING_FACTOR
        return cohesion_x, cohesion_y
    
    def lerp(self, target_x, target_y, alpha):
        self.x = (1.0 - alpha) * self.x + alpha * target_x
        self.y = (1.0 - alpha) * self.y + alpha * target_y


    def update(self):
        if self.x < 150:
            self.dx += TURN_FACTOR
        if self.y < 100:
            self.dy += TURN_FACTOR
        if self.x > SCREEN_WIDTH-150:
            self.dx -= TURN_FACTOR
        if self.y > SCREEN_HEIGHT-100:
            self.dy -= TURN_FACTOR

        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0
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
        self.x += self.dx
        self.y += self.dy