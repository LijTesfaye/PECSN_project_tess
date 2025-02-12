/*
 * CustomRandomWaypointMobility.h
 *  Created on: Jan 2, 2025
 *  Author: Tesfaye
 */
#ifndef MOBILITYMODULE_H_
#define MOBILITYMODULE_H_
//
#include <inet/mobility/single/RandomWaypointMobility.h>
#include <vector>
#include "inet/common/geometry/common/Coord.h"
#include <omnetpp.h>
#include "inet/mobility/contract/IMobility.h"
//
using namespace omnetpp;
using namespace inet;
using namespace std;

class CustomRandomWaypointMobility : public RandomWaypointMobility {

  protected:
    virtual void initialize() override;
    virtual void setInitialPosition() override; // Override the method from the MobilityBase.h

  public:
    CustomRandomWaypointMobility() {};
    virtual ~CustomRandomWaypointMobility() {};

  private:
    int totalCars;
    std::vector<Coord> carInitPositionsList;  // List of car positions to check for overlap
    double minDistance;  // Minimum allowed distance between cars for initialization.

};
#endif /* MOBILITYMODULE_H_ */

