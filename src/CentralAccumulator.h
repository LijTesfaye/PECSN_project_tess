/*
 * CentralAccumulator.h
 *
 *  Created on: Jan 5, 2025
 *      Author: mesay
 */

#ifndef CENTRALACCUMULATOR_H_
#define CENTRALACCUMULATOR_H_

#include <omnetpp.h>
using namespace omnetpp;

class CentralAccumulator : public cSimpleModule
{
  private:
    int totalCars;
    int totalVehiclesSensed;
    double totalSensingRate;

  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    virtual void finish() override;

  public:
    void collectData(int vehiclesSensed, double sensingRate);
};



#endif /* CENTRALACCUMULATOR_H_ */
