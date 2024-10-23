import matplotlib.pyplot as plt
import numpy as np

class Room:


    def __init__(self, width, height, walls=None):
        """
        Initialize the room with width, height, and optional interior walls.

        :param width: Width of the room
        :param height: Height of the room
        :param walls: List of walls, each represented as ((x1, y1), (x2, y2)) line segments
        """
        self.width = width
        self.height = height
        self.walls = walls if walls is not None else []


    def add_wall(self, start_point, end_point):
        """
        Add a wall inside the room.

        :param start_point: (x1, y1) start point of the wall
        :param end_point: (x2, y2) end point of the wall
        """
        self.walls.append((start_point, end_point))

    def draw(self, robot_position=None):
        """
        Draw the room, walls, and optionally a robot's position.

        :param robot_position: Optional tuple (x, y) representing the robot's position.
        """
        plt.clf()
        plt.xlim(0, self.width)
        plt.ylim(0, self.height)

        # Draw the outer boundary of the room
        plt.plot([0, self.width, self.width, 0, 0], [0, 0, self.height, self.height, 0], 'k-', lw=2)

        # Draw walls inside the room
        for wall in self.walls:
            start, end = wall
            plt.plot([start[0], end[0]], [start[1], end[1]], 'r-', lw=2)

        # Draw the robot if its position is given
        if robot_position:
            plt.plot(robot_position[0], robot_position[1], 'bo', markersize=10, label='Robot')

        plt.gca().set_aspect('equal', adjustable='box')
        plt.title("2D Room with Robot")
        plt.legend()
        plt.pause(5.0)


# Example of how to initialize and draw a room
if __name__ == "__main__":
    room = Room(10, 8)
    room.add_wall((2, 2), (2, 6))  # Example wall
    room.add_wall((4, 1), (8, 1))  # Example wall

    room.draw(robot_position=(5, 5))  # Initial robot position
    plt.show()
