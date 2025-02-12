package pecsn_project_tess;
//
//
simple SensingModule
{
    parameters:
        int carID; // Index of this car
        int totalCars; // Total number of cars in the simulation
        double communicationRange @unit(m) = default(50m); // Communication range
        double alphaValue  = default(0.001); // ∝
        double sensingInterval @unit(s) = default(1s); //
        // file 
        string outputFile; // csv file to save the sensing related statistics.
        //
        @signal[sensedVehiclesSignal](type=int);
        @statistic[rateOfSensedVehiclesStat](source="sensedVehiclesSignal"; record=vector;);
        @class(SensingModule);
        
//    gates:
//        output out; // Output gate to the Car's inout gate     
// 
}
