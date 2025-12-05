#include "driver_control.hpp"

#include "lemlib/api.hpp"
#include "main.h"
#include "pros/misc.h"
#include "scoring.hpp"

void DriverControl::split_arcade_drive(int drive_velocity, int turn_velocity) {
    int drive_command{controller_.get_analog(pros::E_CONTROLLER_ANALOG_LEFT_Y) *
                      drive_velocity / 100};
    int turn_command{controller_.get_analog(pros::E_CONTROLLER_ANALOG_RIGHT_X) *
                     turn_velocity / 100};

    chassis_.arcade(drive_command, turn_command, true);
}

void DriverControl::mechanism_control() {
    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_R1)) {
        scoring_.intake();
    } else if (!controller_.get_digital(pros::E_CONTROLLER_DIGITAL_R1)) {
        scoring_.stop_intaking();
    }

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_R2)) {
        scoring_.score(Scoring::ScoreTarget::Low);
    } else if (!controller_.get_digital(pros::E_CONTROLLER_DIGITAL_R2)) {
        scoring_.stop_scoring(Scoring::ScoreTarget::Low);
    }

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_L2)) {
        scoring_.score(Scoring::ScoreTarget::High);
    } else if (!controller_.get_digital(pros::E_CONTROLLER_DIGITAL_L2)) {
        scoring_.stop_scoring(Scoring::ScoreTarget::High);
    }

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_L1)) {
        scoring_.score(Scoring::ScoreTarget::Middle);
    } else if (!controller_.get_digital(pros::E_CONTROLLER_DIGITAL_L1)) {
        scoring_.stop_scoring(Scoring::ScoreTarget::Middle);
    }
}
