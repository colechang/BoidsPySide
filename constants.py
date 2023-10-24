# Define the parameters for the boids simulation
NUM_BOIDS = 800
BOID_SIZE = 2

INTERPOLATION_ALPHA = 0.1

# Tunable parameters (0.0 - 1.0)
AVOID_FACTOR = 0.05     # Increase to encourage more avoidance
MATCHING_FACTOR = 0.05 # Increase to encourage more alignment
CENTERING_FACTOR = 0.00005  # Increase to encourage more cohesion
TURN_FACTOR = 0.3  # Reduce to make turns less aggressive
MAX_SPEED = 10.0  # Reduce to limit maximum speed
MIN_SPEED = 5.0  # Minimum speed

# Viewing and collision avoidance distances
VIEWING_DISTANCE = 30.0
PROTECTED_RANGE = 8.0

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600