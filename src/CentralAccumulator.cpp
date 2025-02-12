#include "CentralAccumulator.h"

Define_Module(CentralAccumulator);
void CentralAccumulator::initialize()
{
    totalCars = par("totalCars");
    totalVehiclesSensed = 0;
    totalSensingRate = 0.0;
}

//
void CentralAccumulator::handleMessage(cMessage *msg)
{
    EV << "[CentralAccumulator] Received message: " << msg->getName() << "\n";
    if (!msg->hasPar("vehiclesSensed") || !msg->hasPar("sensingRate") || !msg->hasPar("carID")) {
        EV << "Message missing required parameters. Discarding.\n";
        delete msg;
        return;
    }

    int carID = msg->addPar("carID");
    int vehiclesSensed = msg->par("vehiclesSensed");
    totalVehiclesSensed += vehiclesSensed;
    double sensingRate = msg->par("sensingRate").doubleValue();
    totalSensingRate += sensingRate;
    EV << "[CentralAccumulator]:"
            " carID: " << carID
            << ", vehiclesSensed: " << vehiclesSensed
            << ", sensingRate: " << sensingRate << "\n";
    // clean up
    delete msg;
}

//
void CentralAccumulator::finish() {
    EV << "[CentralAccumulator] Final Results:\n";
    EV << "  Total Cars in Simulation: " << totalCars << "\n";
    EV << "  Total Vehicles Sensed by All Cars: " << totalVehiclesSensed << "\n";
    EV << "  Total Sensing Rate Sum: " << totalSensingRate << "\n";
    EV << "  Average Sensing Rate per Car: " << (totalCars > 0 ? totalSensingRate / totalCars : 0.0) << "\n";
}
