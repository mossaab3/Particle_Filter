import numpy as np

class Robot:
    def __init__(self, x=0, y=0, theta=0):
        self.x = x
        self.y = y
        self.theta = theta  # Orientation in radians

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self, dtheta):
        self.theta += dtheta

    def get_position(self):
        return (self.x, self.y, self.theta)

    def lidar_scan(self, walls, max_range=10, resolution=360):
        """ Simulates a 360-degree LiDAR scan with a given resolution.
        - walls: list of wall segments [(x1, y1, x2, y2), ...]
        - max_range: maximum sensing range of the LiDAR
        - resolution: number of rays (e.g., 360 for 1 degree steps)
        """
        angles = np.linspace(0, 2 * np.pi, resolution)  # Angles from 0 to 2π
        distances = np.full(resolution, max_range)  # Initialize distances to max_range
        
        for i, angle in enumerate(angles):
            ray_x = self.x
            ray_y = self.y
            for wall in walls:
                x1, y1, x2, y2 = wall
                intersection = self._ray_wall_intersection(ray_x, ray_y, angle, x1, y1, x2, y2)
                if intersection:
                    distance = np.hypot(intersection[0] - self.x, intersection[1] - self.y)
                    distances[i] = min(distances[i], distance)

        return distances + np.random.normal(0, 0.05, resolution)  # Adding noise to each distance

    def _ray_wall_intersection(self, rx, ry, angle, x1, y1, x2, y2):
        """ Calculate intersection between a ray and a wall segment.
        - rx, ry: ray origin (robot's position)
        - angle: ray angle
        - x1, y1, x2, y2: wall segment coordinates
        Returns: (ix, iy) intersection point or None if no intersection.
        """
        dx = np.cos(angle)
        dy = np.sin(angle)

        denom = (x1 - x2) * dy - (y1 - y2) * dx
        if denom == 0:
            return None  # Parallel, no intersection

        t = ((x1 - rx) * dy - (y1 - ry) * dx) / denom
        u = -((x1 - x2) * (y1 - ry) - (y1 - y2) * (x1 - rx)) / denom

        if 0 <= t <= 1 and u >= 0:
            ix = x1 + t * (x2 - x1)
            iy = y1 + t * (y2 - y1)
            return (ix, iy)

        return None
