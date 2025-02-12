#ifndef __PECSN_PROJECT_TESS_POSITIONLOGGER_H_
#define __PECSN_PROJECT_TESS_POSITIONLOGGER_H_

#include <omnetpp.h>
#include "inet/common/INETDefs.h"
#include "inet/common/geometry/common/Coord.h"
#include <fstream>

using namespace omnetpp;
using namespace inet;

class PositionLogger : public cSimpleModule, cListener {

  private:
    int totalCars;               // Total number of cars
    std::string outputFileName;      // Output file name
    std::ofstream outputFileStream;  // File stream for writing position data

  protected:
    virtual void initialize() override;
    virtual void receiveSignal(cComponent *source, simsignal_t signalID, cObject *obj, cObject *details) override;
    virtual void finish() override;

    //void logPosition(const std::string &carID, const Coord &position);
};
#endif

