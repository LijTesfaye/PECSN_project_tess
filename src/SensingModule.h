/////////////////////
#ifndef SENSINGMODULE_H
#define SENSINGMODULE_H
#include <omnetpp.h>
#include <vector>
#include "inet/mobility/contract/IMobility.h"
#include <fstream>
// These name-spaces are useful in the .h and the .cpp files
using namespace omnetpp;
using namespace inet;

class SensingModule : public cSimpleModule
{
  private:
    int carID; //carID
    int totalCars;
    double sensingInterval ; // T
    double communicationRange; // M
    double alphaValue; // ∝
    cMessage *sensingTimer;
    simsignal_t sensedVehiclesSignal;

    // file related
    std::string outputFileName;      // Output file name
    std::ofstream outputFileStream;  // File stream for writing the sensed data

    //
    const char* activeConfigName ;
    std::string folderName ;

  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    void performSensing();
    virtual void finish() override;

  public:
    SensingModule();
    virtual ~SensingModule();

};
#endif // SENSINGMODULE_H

