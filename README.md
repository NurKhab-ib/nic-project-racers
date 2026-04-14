# Neuroevolution of Autonomous Racers: Death-and-Reset AI Car Control
### Authors:
* Makar Vavilov
* Yaroslav Malykh
* Nurbek Khabibullin

This project is a **`pygame`-based racing simulation** in which a population of autonomous cars learns to drive around handcrafted tracks using **neuroevolution**: each car reads the road with virtual sensors, feeds this data into a small neural network, and then improves over generations through `selection`, `crossover`, and `mutation`, while the **death-and-reset** loop restarts failed agents and highlights how behavior gradually evolves toward faster checkpoint collection and completed laps on **3 different maps**.

## What is implemented

- **3 predefined maps** with different geometry (`1`, `2`, `3` keys to switch).
- **Population-based learning** with `POPULATION_SIZE = 50`.
- **Neural controller** per car:
  - inputs: 7 distance sensors + normalized speed,
  - hidden layer: 8 neurons (ReLU),
  - outputs: gas, steering, brake (tanh).
- **Genetic algorithm**:
  - tournament parent selection,
  - per-weight crossover,
  - adaptive mutation (stronger mutation when progress stagnates).
- **Death-and-reset training loop**:
  - generation ends when all cars are dead or time limit is reached,
  - best individuals are kept (`ELITE_SIZE = 5`),
  - new generation starts from the same spawn point and start angle.

## Project structure

- `main.py` - simulation loop, rendering, keyboard controls, generation timer.
- `track.py` - track mask generation, checkpoints, lap/progress counting.
- `car.py` - physics, sensors, neural forward pass, rendering of cars/sensors.
- `evolution.py` - fitness calculation, selection, crossover, mutation, reset.
- `config.py` - all tunable constants (physics, NN size, GA hyperparameters).

## Requirements

- Python 3.10+ (recommended)
- `pygame`
- `numpy`

Install dependencies:

```bash
pip install pygame numpy
```

## Run

From the project root:

```bash
python main.py
```

## Controls

- `SPACE` - pause/unpause
- `H` - show/hide on-screen statistics
- `1` - first track
- `2` - second track
- `3` - third track

## Training logic (short)

1. Cars read distances to track borders using 7 ray sensors.
2. Neural network outputs gas, steering and brake values.
3. Car receives fitness for checkpoint progress and completed laps.
4. At generation end, top individuals survive and produce offspring.
5. Population resets to start; repeat for the next generation.

## Useful parameters to tune

Open `config.py` to experiment:

- **Driving dynamics:** `MAX_SPEED`, `ACCELERATION`, `STEERING_ANGLE`
- **Sensors:** `SENSOR_ANGLES`, `SENSOR_MAX_DISTANCE`
- **Evolution:** `POPULATION_SIZE`, `MUTATION_RATE`, `ELITE_SIZE`, `TOURNAMENT_SIZE`
- **Network size:** `INPUT_SIZE`, `HIDDEN_SIZE`, `OUTPUT_SIZE`

Also in `main.py`:

- `self.gen_limit = 20` - generation duration in seconds.
