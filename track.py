import pygame
import math
from config import *


class Track:
    def __init__(self, path_points):
        self.path_points = path_points
        self.checkpoints = self._build_checkpoints()

        mask_surface = pygame.Surface((WIDTH, HEIGHT))
        mask_surface.fill((0, 0, 0))

        for i in range(len(path_points) - 1):
            pygame.draw.line(mask_surface, (255, 255, 255),
                             path_points[i], path_points[i + 1], TRACK_WIDTH)
        for pt in path_points:
            pygame.draw.circle(mask_surface, (255, 255, 255), pt, TRACK_WIDTH // 2)

        self.track_surface = mask_surface
        self.mask = pygame.mask.from_threshold(mask_surface, (255, 255, 255), (1, 1, 1))

    def _build_checkpoints(self):
        pts = []
        for i in range(len(self.path_points) - 1):
            x1, y1 = self.path_points[i]
            x2, y2 = self.path_points[i + 1]
            n = max(1, int(math.hypot(x2 - x1, y2 - y1) / 40))
            for j in range(n):
                if i == 0 and j == 0:
                    continue
                t = j / n
                pts.append((int(x1 + t * (x2 - x1)), int(y1 + t * (y2 - y1))))
        return pts

    def is_on_track(self, x, y):
        ix, iy = int(x), int(y)
        if not (0 <= ix < WIDTH and 0 <= iy < HEIGHT):
            return False
        return self.mask.get_at((ix, iy))

    def check_checkpoint(self, car):
        if car.checkpoints_reached >= len(self.checkpoints):
            car.laps_completed += 1
            car.checkpoints_reached = 0

        cp = self.checkpoints[car.checkpoints_reached]
        if math.hypot(car.x - cp[0], car.y - cp[1]) < TRACK_WIDTH * 0.6:
            car.checkpoints_reached += 1

    def draw(self, screen):
        screen.blit(self.track_surface, (0, 0))
        if DRAW_CHECKPOINTS:
            for cp in self.checkpoints:
                pygame.draw.circle(screen, GREEN, cp, 3)
        pygame.draw.circle(screen, BLUE, self.path_points[0], 8)
