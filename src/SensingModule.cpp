#include <fstream> // For writing to CSV
#include <sstream>
#include <iomanip>
#include "SensingModule.h"

Define_Module(SensingModule);

SensingModule::SensingModule() :
        sensingTimer(nullptr) {
}

SensingModule::~SensingModule() {
    cancelAndDelete(sensingTimer);
}

void SensingModule::initialize() {

    // Let's bind all the parameters to class members
    carID = par("carID");
    alphaValue = par("alphaValue").doubleValue();
    totalCars = par("totalCars");
    communicationRange = par("communicationRange").doubleValue();
    sensingInterval = alphaValue * communicationRange * communicationRange; // Apply custom value for the 'sensingInterval'
    //
    std::string baseFileName = par("outputFile");

    //
    const char *simTimeLimitStr = getEnvir()->getConfig()->getConfigValue(
            "sim-time-limit");
    simtime_t simTimeLimit =
            (simTimeLimitStr && *simTimeLimitStr) ?
                    SimTime::parse(simTimeLimitStr) : SimTime::getMaxTime();

    // register the signal that was defined in the NED file.
    sensedVehiclesSignal = registerSignal("sensedVehiclesSignal");

    //
    sensingTimer = new cMessage("sensingTimer");

    EV << "Car[" << carID << "]: Alpha = " << alphaValue << ", Range = "
              << communicationRange << ", SensingInterval = " << sensingInterval
              << "s\n";
    //
    EV_INFO << "{Init} Car[" << carID << "] scheduled sensingTimer at "
                   << sensingInterval << " seconds.\n";
    //
    int runNumber = getEnvir()->getConfigEx()->getActiveRunNumber(); // Get the current run number
    // grab the config name
    activeConfigName = getSimulation()->getEnvir()->getConfigEx()->getActiveConfigName();
    EV << "Current configuration: " << activeConfigName << endl;

    // warmupTime_Test
    if (strcmp(activeConfigName, "overAllRate") == 0) {
        folderName = "sensingResults/overAllRate"; // Folder name for the results in the overAllRate INI conf
        }
    else if (strcmp(activeConfigName, "warmupTime_Test") == 0) {
        folderName = "sensingResults/warmupTime_Test"; // Folder name for the results in the warmupTime_Test
        }
    // Consistency
    else if (strcmp(activeConfigName, "Ver_Consistency_Test1") == 0) {
        folderName = "sensingResults/Consistency_Test1"; // Folder name for the results in the Consistency_Test1
        }
    else if (strcmp(activeConfigName, "Ver_Consistency_Test2") == 0) {
        folderName = "sensingResults/Consistency_Test2"; // Folder name for the results in the Consistency_Test2
        }
    // Continuity
    else if (strcmp(activeConfigName, "Ver_Continuity_Test1") == 0) {
        folderName = "sensingResults/Continuity_Test1"; // Folder name for the results in the Continuity_Test1
        }
    else if (strcmp(activeConfigName, "Ver_Continuity_Test2") == 0) {
        folderName = "sensingResults/Continuity_Test2"; // Folder name for the results in the Continuity_Test2
        }

    else if (strcmp(activeConfigName, "Ver_Continuity_Test3") == 0) {
        folderName = "sensingResults/Continuity_Test3"; // Folder name for the results in the Continuity_Test3
        }
    // Degeneracy
    else if (strcmp(activeConfigName, "Ver_Degeneracy_Test1")==0){
        folderName = "sensingResults/Degeneracy_Test1"; // Folder name for the results in the Degeneracy_Test1
        }
    else if (strcmp(activeConfigName, "Ver_Degeneracy_Test2")==0){
        folderName = "sensingResults/Degeneracy_Test2"; // Folder name for the results in the Degeneracy_Test2
        }
    else if (strcmp(activeConfigName, "Ver_Degeneracy_Test3") == 0){
        folderName = "sensingResults/Degeneracy_Test3"; // Folder name for the results in the Degeneracy_Test3
        }
    // Monotonicity
    else if (strcmp(activeConfigName, "Ver_Monotonicity_Test1") == 0) {
        folderName = "sensingResults/Monotonocity_Test1"; // Folder name for the results in the Monotonocity_Test1
        }
    else if (strcmp(activeConfigName, "Ver_Monotonicity_Test2") == 0) {
        folderName = "sensingResults/Monotonocity_Test2"; // Folder name for the results in the Monotonocity_Test2
        }
    else if (strcmp(activeConfigName, "Ver_Monotonicity_Test3") == 0) {
        folderName = "sensingResults/Monotonocity_Test3"; // Folder name for the results in the Monotonocity_Test3
        }
    else if (strcmp(activeConfigName, "Ver_Monotonicity_Test4") == 0) {
        folderName = "sensingResults/Monotonocity_Test4"; // Folder name for the results in the Monotonocity_Test3
        }

    else if (strcmp(activeConfigName, "Ver_Theo_E_N_Test1") == 0) {
        folderName = "sensingResults/Theoretical_Test1"; // Folder name for the results in the Theoretical_Test1
        }

    else if (strcmp(activeConfigName, "Ver_Theo_E_N_Test2") == 0) {
        folderName = "sensingResults/Theoretical_Test2"; // Folder name for the results in the Theoretical_Test2
        }

    else if (strcmp(activeConfigName, "Ver_Theo_E_N_Test3") == 0) {
        folderName = "sensingResults/Theoretical_Test3"; // Folder name for the results in the Theoretical_Test3
        }

    else if (strcmp(activeConfigName, "Ver_Theo_E_N_Test4") == 0) {
        folderName = "sensingResults/Theoretical_Test4"; // Folder name for the results in the Theoretical_Test4
        }

     else {
        throw cRuntimeError("Unknown configuration: %s", activeConfigName);
     }

    // Ensure base folder exists.
    if (_mkdir("sensingResults") && errno != EEXIST) {
        throw cRuntimeError("Failed to create base directory: sensingResults");
    }
    // Create the specific folder
    if (_mkdir(folderName.c_str()) && errno != EEXIST) {
        throw cRuntimeError("Failed to create directory: %s", folderName.c_str());
    }
    // Set Some precision
    std::ostringstream stream;
    stream << folderName << "/" << baseFileName << "_run" << runNumber << "_"
            << std::fixed << std::setprecision(3) << alphaValue << "_"
            << std::fixed << std::setprecision(0) << communicationRange
            << ".csv";

    outputFileName = stream.str();
    // Static flag to ensure the header is written only once
    static bool headerWritten = false;

    // Open the file in append mode
    outputFileStream.open(outputFileName, std::ios::out | std::ios::app);
    if (!outputFileStream.is_open()) {
        throw cRuntimeError("Cannot open file: %s", outputFileName.c_str());
    }

    // Write the header only if it hasn't been written yet
    if (!headerWritten) {
        outputFileStream << "SimulationTime,runNumber,CarID,count,rate\n";
        headerWritten = true;
    }

    EV << "simTimeLimit-limit is: " << simTimeLimit << "\n";
    if (SimTime(sensingInterval) > simTimeLimit) {
        EV_WARN << "Car[" << carID << "]: Sensing interval (" << sensingInterval
                       << "s) exceeds simulation time limit (" << simTimeLimit
                       << "s). Timer will not be scheduled.\n";
        return; // Skip scheduling the timer
    }
    scheduleAt(simTime() + sensingInterval, sensingTimer);
}

//
void SensingModule::handleMessage(cMessage *msg) {
    //
    if (sensingInterval <= 0) {
        throw cRuntimeError("Car[%d]: Invalid sensingInterval = %f", carID,
                sensingInterval);
        return;
    }

    if (msg == sensingTimer) {
        EV_INFO << "Car[" << carID << "] sensing event triggered at time "
                       << simTime() << "\n";
        performSensing();
        // Reschedule the sensing timer for the next cycle
        scheduleAt(simTime() + sensingInterval, sensingTimer);
    } else {
        EV << "Received unexpected message: " << msg->getName() << "\n";
        delete msg;
        //return;
    }
}


/**
 * Handle the Sensing Logic
 *
 */

void SensingModule::performSensing() {
    // Grab the warmup-time
    simtime_t warmupPeriod = getSimulation()->getWarmupPeriod();
    if (simTime() < warmupPeriod) {
        EV_INFO << "Skipping sensing during warmup period (current time: "
                       << simTime() << " < warmup period: " << warmupPeriod
                       << ")\n";
        return;
    }

    cModule *mobilityModule = getParentModule()->getSubmodule("customMobility");
    if (!mobilityModule) {
        EV << "customMobility submodule NOT found!\n";
        return;
    }

    EV<<"customMobility submodule found!\n";
    auto mobility = dynamic_cast<IMobility*>(mobilityModule);
    if (!mobility) {
        EV << "customMobility is NOT  of type IMobility!\n";
        return;
    }

    EV << "customMobility IS of type IMobility!\n";
    // Get the current position of this car.
    Coord currentPosition = mobility->getCurrentPosition();

    // Let's do the [Option1:-per-car] i.e rate of vehicles sensed per-car basis
    int count = 0; // The number of vehicles sensed in the current sensing event.
    for (int i = 0; i < totalCars; i++) {
        if (i == carID)
            continue; // Skip to next car if self sensing occurs.
        cModule *otherCarModule =
                getParentModule()->getParentModule()->getSubmodule("car", i);
        if (!otherCarModule) {
            EV << "otherCarModule submodule NOT found!\n";
            return;
        }

        auto otherCarMobility = check_and_cast<IMobility*>(
                otherCarModule->getSubmodule("customMobility"));
        if (!otherCarMobility) {
            EV << "otherCarMobility is NOT  of type IMobility!\n";
            return;
        }

        Coord otherCarPosition = otherCarMobility->getCurrentPosition();
        double distance = currentPosition.distance(otherCarPosition);
        //
        if (distance <= communicationRange) {
            count++;
        }

        EV_INFO << "Car[" << carID << "] sensing car[" << i << "] at position "
                       << otherCarPosition << ", distance = " << distance
                       << "\n";

    }

    //
    // Grab the simulation run i.e the (repetition x parameter sweep)
    int runNumber = getEnvir()->getConfigEx()->getActiveRunNumber();
    EV_INFO << "runNumber is :" << runNumber << '\n';
    EV_INFO << "alpha value :" << alphaValue << '\n';
    EV_INFO << "communication range value :" << communicationRange << '\n';

    //
    double rate = (sensingInterval > 0) ? (count / sensingInterval) : 0.0000; // Instantaneous sensing_rate per sensing event.
    //
    EV << "Car[" << carID << "] sending " << count << " vehicles sensed ("
              << "at " << sensingInterval << "sec with rate" << rate
              << " per second) to aggregator.\n";

//    // send the data
//    cMessage *msg = new cMessage("SensingData");
//    msg->addPar("carID") = carID;
//    msg->addPar("vehiclesSensed") = count;
//    msg->addPar("sensingRate") = rate;
//    send(msg, "out");
    //
    outputFileStream << simTime() << "," << runNumber << "," << carID << ","
            << count << "," << rate << "\n";
}

void SensingModule::finish() {

    //
    if (outputFileStream.is_open()) {
        EV << "Closing file: " << outputFileName << "\n";
        outputFileStream.close();
    } else {
        EV << "File already closed: " << outputFileName << "\n";
    }

    /*
     if (this == sensingTimer->getOwner()) {
     EV << "Delete sensingTimer" << endl;
     delete sensingTimer;
     }
     cSimpleModule::finish();
     */
}

