from PySide6.QtGui import QColor
# Define the parameters for the boids simulation
NUM_BOIDS = 400
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
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


window_width = 800
window_height = 600