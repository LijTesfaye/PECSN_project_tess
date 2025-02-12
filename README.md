# Problem Definition
## Project 1 – Vehicular network: car sensing
## Project Overview

A vehicular system is composed of **N vehicles** that move randomly within a 2D floorplan of size **L × H**, according to a waypoint model. A waypoint is defined by a pair of coordinates (**x**, **y**) and a speed **s**. The coordinates **x**, **y** are random variables to be defined later. Vehicles move between waypoints **a** and **b** at the constant speed selected together with **b**. As soon as a vehicle reaches a waypoint, it selects a new one and moves towards it.

### Wireless Communication

Vehicles are equipped with a wireless interface and can communicate with other vehicles falling within their transmission range **M**. Every **T** seconds, each vehicle checks how many cars are within its transmission range. The relationship between **T** and **M** is expressed as:

$$
T = \alpha \times M^2
$$

due to power constraints. Here, **α** represents the efficiency of the wireless interface and can assume values between 0 and 1.

### Evaluation

Evaluate at least the overall rate of vehicles sensed per second for various values of **M** and **α**. At least the following scenario has to be evaluated:

- Uniform distribution of **x** and **y**.

In all cases, it is up to the team to calibrate the scenarios so that meaningful results are obtained.

### Project Deliverables

- **Documentation**: According to the standards set during the lectures.
- **Simulator Code**: The implementation of the simulation model.
- **Presentation**: Up to 10 slides maximum.
