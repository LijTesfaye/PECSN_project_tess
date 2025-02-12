//
// 
package pecsn_project_tess;
//
// TODO auto-generated type
//
simple PositionLogger {
    parameters:
       //int loggingInterval @unit(s); // time interval at which positions are logged
       int totalCars; // Total number of cars in the simulation
       string outputFile; // csv file to save the coordinates
       @class(PositionLogger);
}
