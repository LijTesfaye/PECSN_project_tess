// CarSensingNetwork.ned
package pecsn_project_tess.simulations;
//
import inet.visualizer.common.MobilityVisualizer;  // Correct visualizer for mobility
import pecsn_project_tess.Car;
import pecsn_project_tess.PositionLogger;
import pecsn_project_tess.*;

//
network VehicularSensingNetwork
{
    parameters:
        int numCars = default(10);  // Holds the number of vehicles in the simulation.
        // @display("bgb=500,500");
        @display("bgb=500,500");
    submodules:
        car[numCars]: Car {
                carIndex = index;
                allCars = parent.numCars;
                //@display("bgp=200,200");
                @display("p=155,158");
        }
        
        //        positionLogger: PositionLogger {
        //            totalCars = parent.numCars;
        //            //loggingInterval = 1s; // Log every second
        //            outputFile = "car_positions.csv"; // File to save positions
        //            @display("p=205.632,32.256");
        //        }   
//        
//        accumulator: CentralAccumulator {
//                totalCars = parent.numCars;
//                @display("p=232,20");
//        }
        
        mobilityVisualizer: MobilityVisualizer {
                @display("p=58.464,32.256");
        }
        
//    connections:
//        for i=0..numCars-1 {
//                car[i].carOut --> accumulator.in[i];
//        }     

}
