#include "driver_control.hpp"

#include "lemlib/api.hpp"
#include "main.h"
#include "mechanisms/scoring.hpp"
#include "pros/misc.h"

void DriverControl::split_arcade_drive(int drive_velocity, int turn_velocity) {
    int drive_command{controller_.get_analog(pros::E_CONTROLLER_ANALOG_LEFT_Y) *
                      drive_velocity / 100};
    int turn_command{controller_.get_analog(pros::E_CONTROLLER_ANALOG_RIGHT_X) *
                     turn_velocity / 100};

    chassis_.arcade(drive_command, turn_command, true);
}

void DriverControl::two_controller_mechanism_control() {
    if (secondary_controller_.get_digital_new_press(
            pros::E_CONTROLLER_DIGITAL_DOWN))
        scoring_middle_ = true;

    if (secondary_controller_.get_digital_new_press(
            pros::E_CONTROLLER_DIGITAL_UP))
        scoring_middle_ = false;

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_R1))
        scoring_.intake();

    else if (controller_.get_digital_new_release(
                 pros::E_CONTROLLER_DIGITAL_R1)) {
        scoring_.stop_intaking();

        if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_R2))
            scoring_.score(Scoring::ScoreTarget::Low);
        else if (controller_.get_digital_new_release(
                     pros::E_CONTROLLER_DIGITAL_R2))
            scoring_.stop_scoring(Scoring::ScoreTarget::Low);

        if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_L2) ||
            controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_L1)) {
            if (scoring_middle_)
                scoring_.score(Scoring::ScoreTarget::Middle);
            else
                scoring_.score(Scoring::ScoreTarget::High);
        }

        else if (controller_.get_digital_new_release(
                     pros::E_CONTROLLER_DIGITAL_L2) ||
                 controller_.get_digital_new_release(
                     pros::E_CONTROLLER_DIGITAL_L1)) {
            if (scoring_middle_)
                scoring_.stop_scoring(Scoring::ScoreTarget::Middle);
            else
                scoring_.stop_scoring(Scoring::ScoreTarget::High);
        }

        if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_A))
            loader_.toggle();

        if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_X))
            wing_.toggle();

        if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_DOWN))
            double_park_.toggle();
    }
}

void DriverControl::one_controller_mechanism_control() {
    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_R1))
        scoring_.intake();
    else if (controller_.get_digital_new_release(pros::E_CONTROLLER_DIGITAL_R1))
        scoring_.stop_intaking();

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_R2))
        scoring_.score(Scoring::ScoreTarget::Low);
    else if (controller_.get_digital_new_release(pros::E_CONTROLLER_DIGITAL_R2))
        scoring_.stop_scoring(Scoring::ScoreTarget::Low);

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_L2))
        scoring_.score(Scoring::ScoreTarget::Middle);
    else if (controller_.get_digital_new_release(pros::E_CONTROLLER_DIGITAL_L2))
        scoring_.stop_scoring(Scoring::ScoreTarget::Middle);

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_L1))
        scoring_.score(Scoring::ScoreTarget::High);
    else if (controller_.get_digital_new_release(pros::E_CONTROLLER_DIGITAL_L1))
        scoring_.stop_scoring(Scoring::ScoreTarget::High);

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_A))
        loader_.toggle();

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_X))
        wing_.toggle();

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_DOWN))
        double_park_.toggle();
}
