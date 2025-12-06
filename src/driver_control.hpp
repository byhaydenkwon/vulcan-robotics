#pragma once

#include "lemlib/api.hpp"
#include "main.h"
#include "scoring.hpp"

// TODO see issue #72

/// Driver control class.
class DriverControl {
   public:
    DriverControl(lemlib::Chassis& chassis, pros::Controller& controller,
                  Scoring& scoring, pros::adi::Pneumatics& loader,
                  int drive_velocity, int turn_velocity)
        : chassis_{chassis},
          controller_{controller},
          scoring_{scoring},
          loader_{loader},
          drive_velocity_{drive_velocity},
          turn_velocity_{turn_velocity} {}

    void control_loop() {
        while (true) {
            split_arcade_drive(drive_velocity_, turn_velocity_);
            mechanism_control();
            pros::delay(10);
        }
    }

   private:
    void split_arcade_drive(int drive_velocity, int turn_velocity);
    void mechanism_control();

    int drive_velocity_{100};
    int turn_velocity_{75};

    lemlib::Chassis& chassis_;
    pros::Controller& controller_;

    Scoring& scoring_;
    pros::adi::Pneumatics& loader_;
};
