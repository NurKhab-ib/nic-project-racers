# Neuroevolution of Autonomous Racers: Death-and-Reset AI Car Control
### Authors:
* Makar Vavilov
* Yaroslav Malykh
* Nurbek Khabibullin

This project is a **`pygame`-based racing simulation** in which a population of autonomous cars learns to drive around handcrafted tracks using **neuroevolution**: each car reads the road with virtual sensors, feeds this data into a small neural network, and then improves over generations through `selection`, `crossover`, and `mutation`, while the **death-and-reset** loop restarts failed agents and highlights how behavior gradually evolves toward faster checkpoint collection and completed laps on **3 different maps**.
