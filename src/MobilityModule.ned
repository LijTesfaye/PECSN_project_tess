package pecsn_project_tess;
import inet.mobility.single.RandomWaypointMobility;
//
simple MobilityModule extends RandomWaypointMobility
{
    parameters:
        int totalCars; // Total number of cars in the simulation.
        double minInitDistance @unit(m) = default(20m);// Minimum allowed distance between cars for initial Positions in the playground    
        @class(CustomRandomWaypointMobility);
}
