import pygame
import math
import numpy as np
from config import *

class Car:
    def __init__(self, x, y, angle=0):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 0
        self.alive = True
        self.fitness = 0
        self.checkpoints_reached = 0
        self.laps_completed = 0
        self.time_alive = 0
        self.sensors = [0.0] * len(SENSOR_ANGLES)

        self.brain = {
            'w1': np.random.randn(INPUT_SIZE, HIDDEN_SIZE) * 0.5,
            'b1': np.random.randn(HIDDEN_SIZE) * 0.5,
            'w2': np.random.randn(HIDDEN_SIZE, OUTPUT_SIZE) * 0.5,
            'b2': np.random.randn(OUTPUT_SIZE) * 0.5
        }

    def reset(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 0
        self.alive = True
        self.fitness = 0
        self.checkpoints_reached = 0
        self.laps_completed = 0
        self.time_alive = 0

    def update(self, track):
        if not self.alive:
            return

        self.time_alive += 1
        self._read_sensors(track)
        out = self._think()

        # the network outputs control gas, steering, and brakes
        gas = (out[0] + 1) / 2
        self.speed += gas * ACCELERATION
        self.speed = min(self.speed, MAX_SPEED)

        brake = (out[2] + 1) / 2
        self.speed *= (1 - brake * 0.2)

        self.angle += out[1] * STEERING_ANGLE
        self.angle %= 360

        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))

        if not track.is_on_track(self.x, self.y):
            self.alive = False

        track.check_checkpoint(self)

    def _read_sensors(self, track):
        for i, offset in enumerate(SENSOR_ANGLES):
            rad = math.radians(self.angle + offset)
            cos_r, sin_r = math.cos(rad), math.sin(rad)

            # cast each ray until it leaves the track
            for d in range(10, SENSOR_MAX_DISTANCE, 5):
                if not track.is_on_track(self.x + d * cos_r, self.y + d * sin_r):
                    self.sensors[i] = d / SENSOR_MAX_DISTANCE
                    break
            else:
                self.sensors[i] = 1.0

    def _think(self):
        h = np.maximum(0, np.dot(self.sensors + [self.speed / MAX_SPEED], self.brain['w1']) + self.brain['b1'])
        return np.tanh(np.dot(h, self.brain['w2']) + self.brain['b2'])

    def draw(self, screen, is_best=False):
        if not self.alive:
            return

        surf = pygame.Surface(CAR_SIZE, pygame.SRCALPHA)
        surf.fill(GREEN if is_best else RED)
        rotated = pygame.transform.rotate(surf, -self.angle)
        screen.blit(rotated, rotated.get_rect(center=(int(self.x), int(self.y))))

        if DRAW_SENSORS:
            for i, offset in enumerate(SENSOR_ANGLES):
                rad = math.radians(self.angle + offset)
                dist = self.sensors[i] * SENSOR_MAX_DISTANCE
                ex = self.x + dist * math.cos(rad)
                ey = self.y + dist * math.sin(rad)
                k = int(255 * (1 - self.sensors[i]))
                pygame.draw.line(screen, (k, 255 - k, 0),
                                 (int(self.x), int(self.y)), (int(ex), int(ey)), 2)

    def copy(self):
        c = Car(self.x, self.y, self.angle)
        c.brain = {k: v.copy() for k, v in self.brain.items()}
        return c
