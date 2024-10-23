import matplotlib.pyplot as plt
import numpy as np
from robot import Robot
from math import cos, sin


class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.robot = Robot(width / 2, height / 2)  # Start robot in the center
        self.fig, self.ax = plt.subplots()
        self.new_theta = self.robot.theta
        # Define walls as line segments (x1, y1, x2, y2)
        self.walls = [
            (5, 5, 5, 6),  # Example wall from (5, 5) to (5, 6)
            (2, 2, 3, 2),  # Another wall from (2, 2) to (3, 2)
            (7, 8, 8, 8),  # Another wall from (7, 8) to (8, 8)
        ]

    def draw(self):
        self.ax.clear()  # Clear the plot before drawing a new frame
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)

        # Draw environment walls
        self.ax.plot([0, 0, self.width, self.width, 0], [0, self.height, self.height, 0, 0], 'k-')
        for wall in self.walls:
            x1, y1, x2, y2 = wall
            self.ax.plot([x1, x2], [y1, y2], 'k-', lw=3)  # Draw walls as black lines

        # Draw the robot
        self.ax.plot(self.robot.x, self.robot.y, 'ro')  # Robot represented as a red dot

        # Draw LiDAR readings
        distances = self.robot.lidar_scan(self.walls)
        angles = np.linspace(0, 2 * np.pi, len(distances))
        lidar_x = self.robot.x + distances * np.cos(angles)
        lidar_y = self.robot.y + distances * np.sin(angles)
        self.ax.plot(lidar_x, lidar_y, 'b.', markersize=2)  # LiDAR points as blue dots

        self.ax.grid(True)
        plt.draw()

    def update(self):
        self.draw()
        plt.pause(0.01)  # Pause to allow updates in the plot

    def move_robot(self, dx, dy, dtheta=0.0):
        new_x = self.robot.x + dx
        new_y = self.robot.y + dy
        # Only update the position if the new position is within bounds and no wall is hit
        if self.check_bounds(new_x, new_y):
            self.robot.move(dx, dy)
            self.update()

    def check_bounds(self, new_x, new_y):
        """ Check if the robot is within the environment's bounds and not hitting a wall. """
        # Check if the new position is within the environment bounds
        if not (0 <= new_x <= self.width and 0 <= new_y <= self.height):
            return False

        # Check if the new position would intersect with any of the walls
        for wall in self.walls:
            x1, y1, x2, y2 = wall
            # Vertical wall check
            if x1 == x2 and new_x == x1 and min(y1, y2) <= new_y <= max(y1, y2):
                return False
            # Horizontal wall check
            if y1 == y2 and new_y == y1 and min(x1, x2) <= new_x <= max(x1, x2):
                return False

        return True

    def on_key_press(self, event):
        if event.key == 'r':
            self.move_robot(0.0, 0.0, 0.1)
        if event.key == 't':
            self.move_robot(0.1, 0.1)  # Move robot by (0.1, 0.1)
        elif event.key == 'z':
            self.move_robot(0, 0.1)  # Move up
        elif event.key == 'x':
            self.move_robot(0, -0.1)  # Move down
        elif event.key == 'a':
            self.move_robot(-0.1, 0)  # Move left
        elif event.key == 'd':
            self.move_robot(0.1, 0)  # Move right

if __name__ == "__main__":
    env = Environment(10, 10)  # Create a 10x10 grid
    plt.ion()  # Enable interactive mode

    # Connect the key press event to the figure
    env.fig.canvas.mpl_connect('key_press_event', env.on_key_press)

    env.update()  # Initial drawing
    plt.ioff()  # Disable interactive mode when done
    plt.show()  # Keep the window open
