import numpy as np

class Robot:


    def __init__(self, initial_position, max_dimensions=[10.0, 10.0]):
        """
        Initialize the robot in the room.

        :param initial_position: (x, y) initial position of the robot
        :param room: A Room object representing the environment
        """
        self.position = np.array(initial_position)
        self.max_width = max_dimensions[0]
        self.max_height = max_dimensions[1]


    def move(self, delta):
        """
        Move the robot by a given delta.

        :param delta: (dx, dy) change in position
        """
        new_position = self.position + np.array(delta)

        # Ensure robot doesn't move outside the room boundaries
        new_position = np.clip(new_position, [0, 0], [self.max_width, self.max_height])
        self.position = new_position


    def get_position(self):
        """
        Get the current position of the robot.
        """
        return self.position

print("Robot class defined successfully.")
# Example of how to move the robot
if __name__ == "__main__":
    from room import Room

    # Create a room and a robot
    room = Room(10, 8)
    robot = Robot(initial_position=(5, 5), room=room)

    # Simulate moving the robot
    robot.move((1, 0))  # Move right
    robot_position = tuple(robot.get_position())
    room.draw(robot_position=robot_position)
    print("Robot position:", robot.get_position())
