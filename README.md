# Problem Definition
## Project	1 – Vehicular	network:	car	sensing
A vehicular system is composed of N vehicles that move randomly within a
2D floor plan of size L × H, according to a waypoint model. A waypoint is
defined by a pair of coordinates (x,y) and a speed s. The coordinates x, y
are random variables to be defined later. Vehicles move between waypoints
a and b at the constant speed selected together with b. As soon as a vehicle
reaches a waypoint, it selects a new one and moves towards it.
Vehicles are equipped with a wireless interface and can communicate with
other vehicles that fall within their transmission range M. Every T seconds,
each vehicle checks how many cars are within its transmission range. The
relationship between T and M is expressed as in equation 1.
T = α × M2
The α is the efficiency of the wireless interface and can assume values between
0 and 1.
Evaluate at least the overall rate of vehicles sensed per second for various
values of M and α.
At least the following scenario has to be evaluated:
• uniform distribution of x and y;
In all cases, it is up to the team to calibrate the scenarios so that meaningful
results are obtained.
Project deliverables:
(a) Documentation (according to the standards set during the lectures)
1(b) Simulator code
(c) Presentation (up to 10 slides maximum)
