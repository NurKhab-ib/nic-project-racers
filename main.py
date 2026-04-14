import pygame
import sys
import math
from config import *
from track import Track
from evolution import Evolution


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Evolution Car - Genetic Algorithm")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.paused = False
        self.show_stats = True
        self.gen_timer = 0
        self.gen_limit = 20
        self.points = []

        points1 = [
            (150, 400), (200, 250), (350, 150), (550, 100),
            (750, 150), (900, 300), (1000, 450), (950, 620),
            (780, 700), (650, 650), (540, 600), (430, 675),
            (280, 690), (150, 570), (150, 400),
        ]

        points2 = [
            (200, 350), (400, 150), (575, 75), (800, 125), (900, 200), (775, 450),
            (825, 575), (600, 650), (525, 450), (325, 525), (200, 500),
            (200, 350)
        ]

        points3 = [
            (100, 700), (150, 650), (250, 600), (250, 550), (350, 350), (250, 275), (250, 225), (450, 150),
            (650, 100), (700, 50), (900, 100), (500, 400), (400, 400),
            (325, 550), (400, 625), (150, 750), (100, 700)
        ]

        self.points.append(points1)
        self.points.append(points2)
        self.points.append(points3)

        self.current_map = 0
        self._load_track(self.current_map)

    def run(self):
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def _load_track(self, i):
        self.track = Track(self.points[i])
        self.evolution = Evolution(self.track)

        p0 = self.points[i][0]
        p1 = self.points[i][1]
        self.start_angle = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
        self.evolution.create_initial_population(p0[0], p0[1], self.start_angle)

        self.gen_timer = 0
        self.evolution.generation = 0
        self.evolution.best_fitness = 0

    def _switch_track(self, index):
        self.current_map = index
        self._load_track(self.current_map)

    def _handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif ev.key == pygame.K_h:
                    self.show_stats = not self.show_stats
                elif ev.key == pygame.K_1:
                    self._switch_track(0)
                elif ev.key == pygame.K_2:
                    self._switch_track(1)
                elif ev.key == pygame.K_3:
                    self._switch_track(2)

    def _update(self):
        if self.paused:
            return

        self.gen_timer += 1 / 60
        all_dead = True
        for car in self.evolution.population:
            if car.alive:
                car.update(self.track)
                all_dead = False

        if all_dead or self.gen_timer >= self.gen_limit:
            self.evolution.evaluate_fitness()
            self.evolution.selection()
            sx, sy = self.track.path_points[0]
            self.evolution.reset_population(sx, sy, self.start_angle)
            self.gen_timer = 0

    def _draw(self):
        self.screen.fill(BLACK)
        self.track.draw(self.screen)

        alive = [c for c in self.evolution.population if c.alive]
        leader = max(alive, key=lambda c: (c.laps_completed, c.checkpoints_reached),
                     default=None)
        for car in self.evolution.population:
            car.draw(self.screen, is_best=(car is leader))

        if self.show_stats:
            self._draw_stats(leader)

        if self.paused:
            txt = self.font.render("PAUSED", True, RED)
            self.screen.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        pygame.display.flip()

    def _draw_stats(self, leader):
        pop = self.evolution.population
        alive_n = sum(1 for c in pop if c.alive)
        sec = int(max(0, self.gen_limit - self.gen_timer))
        total_cp = len(self.track.checkpoints)

        if leader:
            progress = leader.laps_completed * total_cp + leader.checkpoints_reached
            live_fit = progress * 100
            if leader.laps_completed > 0:
                live_fit += leader.laps_completed * 500000 / max(1, leader.time_alive)
        else:
            live_fit = 0

        lines = [
            f"Gen: {self.evolution.generation}",
            f"Fitness: {live_fit:.0f}  (best: {self.evolution.best_fitness:.0f})",
            f"Alive: {alive_n}/{POPULATION_SIZE}",
            f"Laps: {leader.laps_completed if leader else 0}"
            f" + {leader.checkpoints_reached if leader else 0}/{total_cp}",
            f"Time: {sec}s",
            "",
            "SPACE - Pause | H - Hide",
            "Switch track:",
            "1 - First track",
            "2 - Second track",
            "3 - Third track",
        ]
        y = 10
        for line in lines:
            if line:
                self.screen.blit(self.font.render(line, True, WHITE), (10, y))
                y += 30


if __name__ == "__main__":
    Game().run()
