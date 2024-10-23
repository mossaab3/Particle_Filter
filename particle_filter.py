import numpy as np
import matplotlib.pyplot as plt
import math
import random

class Room:
    def __init__(self, width, height, walls):
        self.width = width
        self.height = height
        self.walls = walls  # List of wall segments (x1, y1, x2, y2)

    def plot(self):
        plt.xlim(0, self.width)
        plt.ylim(0, self.height)
        for wall in self.walls:
            plt.plot([wall[0], wall[2]], [wall[1], wall[3]], 'k-')

class Robot:
    def __init__(self, x, y, theta, sensor_range=10):
        self.x = x
        self.y = y
        self.theta = theta  # Orientation of the robot
        self.sensor_range = sensor_range

    def move(self, delta_x, delta_y, delta_theta):
        self.x += delta_x
        self.y += delta_y
        self.theta += delta_theta

    def sense(self, room):
        distances = []
        for angle in np.linspace(0, 2 * np.pi, num=360):
            ray_direction = [math.cos(self.theta + angle), math.sin(self.theta + angle)]
            distance = self.ray_cast(ray_direction, room)
            distances.append(min(distance, self.sensor_range))
        return distances

    def ray_cast(self, ray_direction, room):
        min_distance = self.sensor_range
        for wall in room.walls:
            intersection, distance = ray_wall_intersection(self.x, self.y, ray_direction, wall, self.sensor_range)
            if intersection:
                min_distance = min(min_distance, distance)
        return min_distance

def ray_wall_intersection(robot_x, robot_y, ray_direction, wall, max_range):
    x1, y1, x2, y2 = wall
    dx_r, dy_r = ray_direction
    wall_dx = x2 - x1
    wall_dy = y2 - y1
    denom = dx_r * (y1 - y2) - dy_r * (x1 - x2)
    if denom == 0:
        return None, max_range
    t = ((robot_x - x1) * (y1 - y2) - (robot_y - y1) * (x1 - x2)) / denom
    u = ((x1 - robot_x) * dy_r - (y1 - robot_y) * dx_r) / denom
    if 0 <= t <= 1 and 0 <= u <= max_range:
        ix = robot_x + u * dx_r
        iy = robot_y + u * dy_r
        return (ix, iy), u
    return None, max_range

class ParticleFilter:
    def __init__(self, num_particles, room, sensor_range):
        self.num_particles = num_particles
        self.particles = self.initialize_particles(room)
        self.weights = np.ones(num_particles) / num_particles
        self.sensor_range = sensor_range

    def initialize_particles(self, room):
        particles = []
        for _ in range(self.num_particles):
            x = random.uniform(0, room.width)
            y = random.uniform(0, room.height)
            theta = random.uniform(0, 2 * np.pi)
            particles.append((x, y, theta))
        return np.array(particles)

    def predict(self, delta_x, delta_y, delta_theta):
        noise = 0.1  # Motion noise
        for i in range(self.num_particles):
            x, y, theta = self.particles[i]
            x += delta_x + random.gauss(0, noise)
            y += delta_y + random.gauss(0, noise)
            theta += delta_theta + random.gauss(0, noise)
            self.particles[i] = (x, y, theta)

    def update(self, robot, room):
        for i in range(self.num_particles):
            x, y, theta = self.particles[i]
            distances = self.get_distances(x, y, theta, room)
            sensor_readings = robot.sense(room)
            self.weights[i] = self.compute_weight(distances, sensor_readings)
        self.weights += 1.e-300  # Avoid divide by zero
        self.weights /= np.sum(self.weights)  # Normalize

    def get_distances(self, x, y, theta, room):
        distances = []
        for angle in np.linspace(0, 2 * np.pi, num=360):
            ray_direction = [math.cos(theta + angle), math.sin(theta + angle)]
            distance = robot.ray_cast(ray_direction, room)
            distances.append(min(distance, self.sensor_range))
        return distances

    def compute_weight(self, particle_distances, actual_sensor_readings):
        # Gaussian probability
        weight = 1.0
        noise = 0.5  # Sensor noise
        for particle_d, actual_d in zip(particle_distances, actual_sensor_readings):
            weight *= self.gaussian(actual_d, noise, particle_d)
        return weight

    @staticmethod
    def gaussian(mu, sigma, x):
        return (1.0 / (sigma * math.sqrt(2.0 * np.pi))) * math.exp(-0.5 * ((x - mu) / sigma) ** 2)

    def resample(self):
        indices = np.arange(self.num_particles)
        new_particles = []
        cumulative_sum = np.cumsum(self.weights)
        for _ in range(self.num_particles):
            random_index = random.uniform(0, 1)
            particle_index = np.searchsorted(cumulative_sum, random_index)
            new_particles.append(self.particles[particle_index])
        self.particles = np.array(new_particles)

    def estimate(self):
        x = np.average(self.particles[:, 0], weights=self.weights)
        y = np.average(self.particles[:, 1], weights=self.weights)
        theta = np.average(self.particles[:, 2], weights=self.weights)
        return (x, y, theta)

# Example Usage
room = Room(10, 10, [(0, 0, 10, 0), (0, 0, 0, 10), (10, 0, 10, 10), (0, 10, 10, 10), (5, 5, 5, 6)])
robot = Robot(2, 2, math.radians(45))

pf = ParticleFilter(num_particles=100, room=room, sensor_range=10)

plt.ion()  # Interactive plot
for _ in range(100):
    robot.move(0.1, 0.1, math.radians(5))  # Simulated robot motion
    pf.predict(0.1, 0.1, math.radians(5))
    pf.update(robot, room)
    pf.resample()

    # Visualization
    plt.clf()
    room.plot()
    plt.scatter(robot.x, robot.y, color='r', label="Robot")
    particles = pf.particles
    plt.scatter(particles[:, 0], particles[:, 1], color='b', s=1, label="Particles")
    plt.pause(0.01)

plt.ioff()
plt.show()
