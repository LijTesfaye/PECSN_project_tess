/*
 * CustomRandomWaypointMobility.cpp
 *
 *  Created on: Jan 2, 2025
 *      Author: Tesfaye
 */
#include "MobilityModule.h"

Define_Module(CustomRandomWaypointMobility);

void CustomRandomWaypointMobility::initialize()
{
    totalCars = par("totalCars");
    minDistance=par("minInitDistance");
}

void CustomRandomWaypointMobility::setInitialPosition()
{
    bool validInitPos = false;
    Coord newPos;

    while (!validInitPos) {
        // Generate random initial position
        double minX = par("constraintAreaMinX").doubleValue();
        double maxX = par("constraintAreaMaxX").doubleValue();
        double minY = par("constraintAreaMinY").doubleValue();
        double maxY = par("constraintAreaMaxY").doubleValue();

        // Generate random initial position
        newPos.x = uniform(minX, maxX);
        newPos.y = uniform(minY, maxY);

        validInitPos = true;
        // Check for overlap with existing cars.
        for (const auto& pos : carInitPositionsList) {
            if (newPos.distance(pos) < minDistance) {
                validInitPos = false;
                break;
            }
        }
    }
    // Add the valid position to the list
    carInitPositionsList.push_back(newPos);

    // Set the car's initial position
    lastPosition = newPos;
}




