# Boids Simulation

## Overview

![Representation of Boids in Nature](image.png)

The Boids Simulation is a Python application that demonstrates the behavior of a flock of birds (boids) in a window. This project uses PySide6 to create a graphical user interface (GUI) for the simulation. Boids are simulated as small circles that move around the screen, mimicking flocking behavior.

<!--![Boids Simulation Screenshot](screenshot.png)-->

## Features

- Simulates the movement of a flock of boids.
- Boids wrap around the screen edges when they reach the boundary.
- Customizable parameters for the simulation, such as the number of boids, their speed, and appearance.
- Real-time rendering of boids using PySide6's QPainter.

## Requirements

- Python 3
- PySide6 library (install with `pip3 install PySide6`)

## How to Run

1. Ensure you have Python 3 and PySide6 installed.

2. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/colechang/BoidsPySide.git
   ```

## References

- https://vergenet.net/~conrad/boids/
- https://vanhunteradams.com/Pico/Animal_Movement/Boids-algorithm.html
