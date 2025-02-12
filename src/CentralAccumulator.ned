package pecsn_project_tess;
//
simple CentralAccumulator
{
    parameters:
        int totalCars; // Number of cars in the simulation
        @display("i=block/cloud");
        @class(CentralAccumulator);
        
    gates:
        input in[totalCars];         
}
