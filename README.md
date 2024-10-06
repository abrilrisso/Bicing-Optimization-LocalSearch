# Bicing-Optimization-LocalSearch

# Local Search for Bicing Optimization

## Project Overview

This project was developed as part of a practical assignment for the course **Basic Algorithms for Artificial Intelligence** at **Universitat Politècnica de Catalunya**. The main goal is to optimize the **Bicing** system, which involves distributing bicycles among various stations in a city. The problem is modeled using **local search algorithms**, such as **Hill Climbing** and **Simulated Annealing**, to solve the bicycle redistribution issue.

## Problem Description

The Bicing system collects and distributes bicycles across stations throughout the city. However, due to varying demand at different times of the day, bicycles tend to accumulate in certain stations, leaving others empty. To address this problem, we use **local search algorithms** to reallocate bicycles using vans that can transport them between stations. The objective is to minimize costs while maximizing user satisfaction by having bicycles available when needed.

### Key Elements:
- **Bicing Stations**: The city is represented as a grid, and bicycles are distributed across various stations. Some stations experience an excess of bicycles, while others face a shortage.
- **Vans**: Vans are used to transport bicycles between stations, with each van having specific capacities and movement constraints.
- **Local Search**: Two algorithms are implemented:
  - **Hill Climbing**: An iterative algorithm that starts with an initial solution and attempts to improve it by applying small changes.
  - **Simulated Annealing**: A probabilistic technique that allows exploring solutions that might initially seem worse, to avoid getting trapped in local optima.

## Experiments

A total of seven experiments were conducted to analyze the performance of the different heuristics, operators, and configurations in solving the Bicing problem:

- **Experiment 1**: Testing the impact of various operators on the solution quality.
- **Experiment 2**: Comparing different initial state generation strategies.
- **Experiment 3**: Tuning parameters for Simulated Annealing, such as temperature decay.
- **Experiment 4**: Varying the number of stations and evaluating the system's scalability.
- **Experiment 5**: Comparing different heuristics for evaluating the quality of the solution.
- **Experiment 6**: Varying the number of vans and analyzing the effect on optimization performance.
- **Experiment 7**: Final experiment combining the most effective strategies for optimal performance.

## Results

The results are displayed via graphs and tables, showcasing the performance of each algorithm and configuration. These can be found in the graficas_experimentos_bicing.ipynb file.

## Conclusion

Through local search algorithms, we were able to optimize the distribution of bicycles in the Bicing system. The experiments demonstrated that combining Simulated Annealing with well-chosen heuristics significantly improves the performance, ensuring that bicycles are distributed efficiently across the city.

