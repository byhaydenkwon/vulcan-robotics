#pragma once

#include "lemlib/api.hpp"
#include "main.h"
#include "mechanisms/scoring.hpp"
#include "pros/adi.hpp"
#include "utils/settings.hpp"

// TODO see issue #72

/// Driver control class.
class DriverControl {
   public:
    DriverControl(Settings& settings, lemlib::Chassis& chassis,
                  pros::Controller& controller, Scoring& scoring,
                  pros::adi::Pneumatics& loader, pros::adi::Pneumatics& wing,
                  pros::adi::Pneumatics& double_park, int drive_velocity,
                  int turn_velocity)
        : settings_{settings},
          chassis_{chassis},
          controller_{controller},
          scoring_{scoring},
          loader_{loader},
          double_park_{double_park},
          wing_{wing},
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

    Settings& settings_;
    lemlib::Chassis& chassis_;
    pros::Controller& controller_;

    Scoring& scoring_;
    pros::adi::Pneumatics& loader_;
    pros::adi::Pneumatics& wing_;
    pros::adi::Pneumatics& double_park_;
};
