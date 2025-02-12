//Car.ned
package pecsn_project_tess;
import inet.mobility.single.RandomWaypointMobility;
//
module Car
{
    parameters:
        @display("i=block/cogwheel;bgb=400,400");
        int carIndex;
        int allCars;
        //Playground Coord Values
        double minCoordValue @unit(m) = default(0m);// the min coordinate value
        double maxCoordValue @unit(m) = default(500m); // the max coordinate value
        // Speed
        double minSpeed @unit(mps) = default(1mps);
        double maxSpeed @unit(mps) = default(10mps);

//    gates:
//        //input carIn; // Gate to expose customSensing's output
//        output carOut;
    submodules:
        //customMobilityX: RandomWaypointMobility {
        customMobility: MobilityModule {
            totalCars = parent.allCars;
            // x
            constraintAreaMinX = parent.minCoordValue;
            constraintAreaMaxX = parent.maxCoordValue;
            // y 
            constraintAreaMinY = parent.minCoordValue;
            constraintAreaMaxY = parent.maxCoordValue;
            //z
            constraintAreaMinZ = 0m;
            constraintAreaMaxZ = 0m;
            //Initials
            initialX = uniform(parent.minCoordValue, parent.maxCoordValue);
            initialY = uniform(parent.minCoordValue, parent.maxCoordValue);
            initialZ = 0m;
            // Choose a uniform speed for each car
            speed = uniform(parent.minSpeed, parent.maxSpeed);
            //
            waitTime = (0s);
            @display("p=$x,$y");
        }
        
        // Custom Sensing Simple Module  
        customSensing: SensingModule {
            carID = parent.carIndex;  // Pass carIndex to customSensing
            totalCars = parent.allCars;
            outputFile = "vehicles_sensed"; // File to save positions
            @display("p=298,101");
        }

//    connections:
//        customSensing.out --> carOut;
}

