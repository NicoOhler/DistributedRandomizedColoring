# Centralized Simulation of a Randomized Distributed Coloring Algorithm

## Description
The goal of this exercise is to provide a centralized implementation that simulates a randomized distributed coloring algorithm. This implementation takes a graph G = (V, E) with maximum degree ∆ as its input and simulates the following distributed randomized (∆ + 1)-coloring algorithm until all vertices are colored.

## Simulated Algorithm
Initially, all nodes are uncolored. Then, in synchronous iterations, each uncolored node selects a random candidate color from its list of available colors, that is, from the set of colors that none of its already permanently colored neighbors have. Then, nodes exchange their candidate colors with their neighbors. A node v that has a candidate color c that is not selected as a candidate color by any of its neighbors gets permanently colored with c, otherwise v discards its candidate color, remains uncolored, and proceeds with the next iteration.

## Setup
To run the simulation, follow these steps:
1. Clone the repository:
    ```
    git clone https://github.com/NicoOhler/RandomizedDistributedColoring.git
    ```
2. Navigate to the project directory:
    ```
    cd RandomizedDistributedColoring
    ```
3. Install the required dependencies:
    ```
    python3 -m pip install networkx
    ```
4. Run the simulation:
    ```
    python3 distributed_randomized_coloring.py
    ```

## Main Function
The main function demonstrates a basic example with a random graph of 300 nodes and 120 degree, displaying all the intermediate steps of the algorithm as debug messages. It further verifies the coloring of the final coloring of the graph. Additionally, a set of test cases on various types of random graphs is executed, ensuring the correctness of the algorithm.
