#pragma once

#include "lemlib/api.hpp"
#include "main.h"
#include "mechanisms/scoring.hpp"
#include "pros/adi.hpp"

// TODO see issue #72

/// Driver control class.
class DriverControl {
   public:
    DriverControl(lemlib::Chassis& chassis, pros::Controller& controller,
                  pros::Controller& secondary_controller, Scoring& scoring,
                  pros::adi::Pneumatics& loader, pros::adi::Pneumatics& wing,
                  pros::adi::Pneumatics& double_park, int drive_velocity,
                  int turn_velocity, bool use_two_controllers)
        : chassis_{chassis},
          controller_{controller},
          secondary_controller_{secondary_controller},
          scoring_{scoring},
          loader_{loader},
          double_park_{double_park},
          wing_{wing},
          drive_velocity_{drive_velocity},
          turn_velocity_{turn_velocity},
          use_two_controllers_{use_two_controllers} {
        if (controller.is_connected() && !secondary_controller.is_connected()) {
            printf("Secondary controller not connected, using only one");
            use_two_controllers_ = false;
        }
    }

    void control_loop() {
        while (true) {
            split_arcade_drive(drive_velocity_, turn_velocity_);
            if (use_two_controllers_)
                two_controller_mechanism_control();
            else
                one_controller_mechanism_control();
            pros::delay(10);
        }
    }

   private:
    void split_arcade_drive(int drive_velocity, int turn_velocity);
    void two_controller_mechanism_control();
    void one_controller_mechanism_control();

    void set_both_text(const char* text);

    int drive_velocity_{100};
    int turn_velocity_{75};

    bool scoring_middle_{false};
    bool intake_flushing_{false};

    // these variables are used to store the status of scoring_middle_
    // and intake_flushing at the time of activation, so that even if
    // the secondary controller switches the mode for either,
    // the release still stops the correct action.
    bool last_scoring_middle_{scoring_middle_};
    bool last_intake_flushing_{intake_flushing_};

    lemlib::Chassis& chassis_;
    pros::Controller& controller_;
    pros::Controller& secondary_controller_;
    bool use_two_controllers_;

    Scoring& scoring_;
    pros::adi::Pneumatics& loader_;
    pros::adi::Pneumatics& wing_;
    pros::adi::Pneumatics& double_park_;
};
