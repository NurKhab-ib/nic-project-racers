import random
import numpy as np
from config import *
from car import Car

class Evolution:
    def __init__(self, track):
        self.track = track
        self.population = []
        self.generation = 0
        self.best_fitness = 0

    def create_initial_population(self, sx, sy, sa):
        self.population = [Car(sx, sy, sa) for _ in range(POPULATION_SIZE)]

    def evaluate_fitness(self):
        n_cp = len(self.track.checkpoints)
        for car in self.population:
            progress = car.laps_completed * n_cp + car.checkpoints_reached
            car.fitness = progress * 100
            if car.laps_completed > 0:
                car.fitness += car.laps_completed * 500000 / max(1, car.time_alive)

    def selection(self):
        self.population.sort(key=lambda c: c.fitness, reverse=True)

        top = self.population[0]
        if top.fitness > self.best_fitness:
            self.best_fitness = top.fitness
            print(f"Gen {self.generation}: fitness={top.fitness:.0f}, "
                  f"laps={top.laps_completed}, cp={top.checkpoints_reached}")

        new_pop = [c.copy() for c in self.population[:ELITE_SIZE]]
        while len(new_pop) < POPULATION_SIZE:
            p1 = self._tournament()
            p2 = self._tournament()
            child = self._crossover(p1, p2)
            self._mutate(child)
            new_pop.append(child)

        self.population = new_pop
        self.generation += 1

    def _tournament(self):
        group = random.sample(self.population, TOURNAMENT_SIZE)
        return max(group, key=lambda c: c.fitness)

    def _crossover(self, p1, p2):
        child = Car(0, 0)
        child.brain = {}
        for key in p1.brain:
            mask = np.random.random(p1.brain[key].shape) < 0.5
            child.brain[key] = np.where(mask, p1.brain[key], p2.brain[key])
        return child

    def _mutate(self, car):
        for key in car.brain:
            m = np.random.random(car.brain[key].shape) < MUTATION_RATE
            car.brain[key] += m * np.random.randn(*car.brain[key].shape) * 0.1

    def reset_population(self, sx, sy, sa):
        for car in self.population:
            car.reset(sx, sy, sa)
