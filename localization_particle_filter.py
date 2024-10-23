import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Room boundaries
ROOM_WIDTH = 10
ROOM_HEIGHT = 10

# Number of particles
NUM_PARTICLES = 100

# Robot motion noise and sensor noise
MOTION_NOISE = 0.5
SENSOR_NOISE = 1.0

# Robot true position
robot_position = np.array([5.0, 5.0])  # initial robot position at the center of the room

# Initialize particles
particles = np.random.rand(NUM_PARTICLES, 2) * [ROOM_WIDTH, ROOM_HEIGHT]  # Randomly distributed particles
weights = np.ones(NUM_PARTICLES) / NUM_PARTICLES  # Initial weights

def move_robot(robot_position, move_command):
    # Apply motion command with noise
    new_position = robot_position + move_command + np.random.randn(2) * MOTION_NOISE
    # Keep robot within room boundaries
    new_position = np.clip(new_position, [0, 0], [ROOM_WIDTH, ROOM_HEIGHT])
    return new_position

def move_particles(particles, move_command):
    # Apply motion command to particles with noise
    particles += move_command + np.random.randn(NUM_PARTICLES, 2) * MOTION_NOISE
    # Keep particles within room boundaries
    particles = np.clip(particles, [0, 0], [ROOM_WIDTH, ROOM_HEIGHT])
    return particles

def sense(robot_position):
    # Simulated sensor measurement (with noise)
    return robot_position + np.random.randn(2) * SENSOR_NOISE

def update_weights(particles, measurement):
    # Update particle weights based on sensor measurement
    distances = np.linalg.norm(particles - measurement, axis=1)
    weights = np.exp(-distances**2 / (2 * SENSOR_NOISE**2))
    weights += 1.e-300  # avoid division by zero
    weights /= sum(weights)  # normalize
    return weights

def resample_particles(particles, weights):
    # Resample particles proportional to their weights
    indices = np.random.choice(np.arange(NUM_PARTICLES), size=NUM_PARTICLES, p=weights)
    resampled_particles = particles[indices]
    return resampled_particles

def estimate_position(particles, weights):
    # Estimate the robot's position as the weighted average of the particles
    return np.average(particles, axis=0, weights=weights)

def plot_particles(particles, robot_position, estimated_position):
    plt.clf()
    plt.xlim(0, ROOM_WIDTH)
    plt.ylim(0, ROOM_HEIGHT)
    
    # Plot particles
    plt.scatter(particles[:, 0], particles[:, 1], s=5, color='blue', alpha=0.5, label='Particles')
    
    # Plot robot true position
    plt.plot(robot_position[0], robot_position[1], 'ro', label='True Position')
    
    # Plot estimated position
    plt.plot(estimated_position[0], estimated_position[1], 'gx', label='Estimated Position')
    
    # Draw room boundaries
    plt.gca().add_patch(plt.Rectangle((0, 0), ROOM_WIDTH, ROOM_HEIGHT, fill=None, edgecolor='black'))
    
    plt.legend()
    plt.pause(0.01)

# Simulate robot movement and particle filter
plt.ion()
for _ in range(50):  # run for 50 steps
    move_command = np.array([0.5, 0.2])  # Constant movement command (move right and up)
    
    # Move robot and sense position
    robot_position = move_robot(robot_position, move_command)
    measurement = sense(robot_position)
    
    # Move particles
    particles = move_particles(particles, move_command)
    
    # Update particle weights based on the sensor measurement
    weights = update_weights(particles, measurement)
    
    # Resample particles based on the updated weights
    particles = resample_particles(particles, weights)
    
    # Estimate robot's position
    estimated_position = estimate_position(particles, weights)
    
    # Plot particles and robot
    plot_particles(particles, robot_position, estimated_position)

plt.ioff()
plt.show()
