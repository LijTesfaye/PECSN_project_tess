#include "PositionLogger.h"
#include "inet/mobility/single/RandomWaypointMobility.h"
#include "inet/mobility/contract/IMobility.h"
#include "inet/common/INETDefs.h"
#include <fstream>

Define_Module(PositionLogger);

void PositionLogger::initialize()
{
    //currentRunNumber = getSimulation()->getRunNumber();
    outputFileName = cSimpleModule::par("outputFile").stringValue();
    // Check if the file exists and is not empty
    std::ifstream checkFile(outputFileName);
    bool isEmpty = checkFile.peek() == std::ifstream::traits_type::eof();
    checkFile.close();
    outputFileStream.open(outputFileName, std::ios::out | (isEmpty ? std::ios::trunc : std::ios::app));

    if (!outputFileStream.is_open()) {
        throw cRuntimeError("Cannot open file: %s", outputFileName.c_str());
    }

    // if empty write the header
    if (isEmpty) {
        outputFileStream << "SimTime,Run,CarID,cPositionX,cPositionY,tPositionX,tPositionY\n";
    }
    //
    totalCars = cSimpleModule::par("totalCars").intValue();
    //
    for(int i = 0; i < totalCars; ++i) {
        cModule *car = getParentModule()->getSubmodule("car", i);
        if(!car){
            throw cRuntimeError("Car module not found at index %d", i);
        }
        cModule *mobility = car->getSubmodule("customMobility");
        if (mobility) {
            mobility->cSimpleModule::subscribe("mobilityStateChanged", this);
        }
    }
}

void PositionLogger::receiveSignal(cComponent *source, simsignal_t signalID, cObject *obj, cObject *details) {
    //
    // Cast the source to RandomWaypointMobility to access its functionality
    auto mobility = dynamic_cast<inet::RandomWaypointMobility *>(source);
    if (mobility) {
        // Access the current position and target position
        Coord currentPosition = mobility->getCurrentPosition();
        Coord targetPosition = mobility->getTargetPosition();  // Access the target position via the getter

        // Log the positions to console (optional)
        EV_INFO << "Current Position: " << currentPosition << ", Target Position: " << targetPosition << "\n";
        // Assuming the car's ID is associated with the parent module's name
        const char *carID = source->getParentModule()->getFullName();

        simtime_t currentSimTime = simTime();
        simtime_t warmupPeriod = getSimulation()->getWarmupPeriod();
        EV_INFO<<"Warmup period is :"<<warmupPeriod<<'\n';
        // Log data to the CSV file: time, carID, current x, current y, target x, target y
        if(currentSimTime>= warmupPeriod) {

            // Check if the car has arrived at the waypoint
            if (currentPosition == targetPosition) {
                EV_INFO << "Car " << carID<< " arrived at waypoint: " << targetPosition << " at time " << simTime() << "\n";
                int runNumber = getEnvir()->getConfigEx()->getActiveRunNumber();
                EV_INFO<<"runNumber is :"<<runNumber<<'\n';
                outputFileStream << currentSimTime << ","                  // Simulation time
                                   << runNumber<< ","                      // run number
                                   << carID << ","                         // Car ID
                                   <<currentPosition.x<< ","               // current X coordinate
                                   <<currentPosition.y<< ","               // current Y coordinate
                                   << targetPosition.x << ","              // target X coordinate
                                   << targetPosition.y << "\n";            // target Y coordinate
                }
        } else {
            EV_DEBUG <<"Skipping logging during warmup period: " << warmupPeriod << "s\n";
        }
    }
}
//
void PositionLogger::finish() {
    if (outputFileStream.is_open()) {
        EV << "Closing file: " << outputFileName << "\n";
        outputFileStream.close();
    } else {
            EV << "File already closed: " << outputFileName << "\n";
    }
}

