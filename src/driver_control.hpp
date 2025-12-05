#pragma once

#include "lemlib/api.hpp"
#include "main.h"
#include "scoring.hpp"

// TODO see issue #72

/// Driver control class.
class DriverControl {
   public:
    DriverControl(lemlib::Chassis chassis, pros::Controller controller,
                  Scoring scoring, pros::adi::Pneumatics aligner,
                  pros::adi::Pneumatics loader)
        : chassis_{chassis},
          controller_{controller},
          scoring_{scoring},
          aligner_{aligner},
          loader_{loader} {}

    control_loop() {
        while (true) {
            split_arcade_drive();
            mechanism_control();
        }
    }

   private:
    void split_arcade_drive(int drive_velocity, int turn_velocity);
    void mechanism_control();

    int drive_velocity{100.0};
    int turn_velocity{75.0};

    lemlib::Chassis chassis_;
    pros::Controller controller_;

    Scoring scoring_;
    pros::adi::Pneumatics aligner;
    pros::adi::Pneumatics loader;
}
