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
    // secondary controller

    // secondary set middle score
    if (secondary_controller_.get_digital_new_press(
            pros::E_CONTROLLER_DIGITAL_DOWN)) {
        scoring_middle_ = true;
        set_both_text("SCORE MID");
    }

    if (secondary_controller_.get_digital_new_press(
            pros::E_CONTROLLER_DIGITAL_UP)) {
        scoring_middle_ = false;
        set_both_text("SCORE MID");
    }

    // secondary set intake flushing
    if (secondary_controller_.get_digital_new_press(
            pros::E_CONTROLLER_DIGITAL_X)) {
        intake_flushing_ = true;
        set_both_text("INTAKE FLUSH");
    }

    if (secondary_controller_.get_digital_new_press(
            pros::E_CONTROLLER_DIGITAL_B)) {
        intake_flushing_ = false;
        set_both_text("INTAKE NORMAL");
    }

    // primary controller

    // low scoring
    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_R2))
        scoring_.score(Scoring::ScoreTarget::Low);
    else if (controller_.get_digital_new_release(pros::E_CONTROLLER_DIGITAL_R2))
        scoring_.stop_scoring(Scoring::ScoreTarget::Low);

    // L1/L2 scoring logic based on secondary status
    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_L2) ||
        controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_L1)) {
        if (scoring_middle_) {
            scoring_.score(Scoring::ScoreTarget::Middle);
            last_scoring_middle_ = true;
        } else {
            scoring_.score(Scoring::ScoreTarget::High);
            last_scoring_middle_ = false;
        }

    } else if (controller_.get_digital_new_release(
                   pros::E_CONTROLLER_DIGITAL_L2) ||
               controller_.get_digital_new_release(
                   pros::E_CONTROLLER_DIGITAL_L1)) {
        if (last_scoring_middle_) {
            scoring_.stop_scoring(Scoring::ScoreTarget::Middle);
        } else {
            scoring_.stop_scoring(Scoring::ScoreTarget::High);
        }
    }

    // R1 intake logic based on secondary status
    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_R1)) {
        if (intake_flushing_) {
            scoring_.score(Scoring::ScoreTarget::Middle);
            last_intake_flushing_ = true;
        } else {
            scoring_.intake();
            last_intake_flushing_ = false;
        }
    } else if (controller_.get_digital_new_release(
                   pros::E_CONTROLLER_DIGITAL_R1)) {
        if (last_intake_flushing_) {
            scoring_.stop_scoring(Scoring::ScoreTarget::Middle);
        } else {
            scoring_.stop_intaking();
        }
    }

    // pneumatics
    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_A))
        loader_.toggle();

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_X))
        wing_.toggle();

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_DOWN))
        double_park_.toggle();
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

/// Set text on the bottom line of both controllers, clearing beforehand
/// to prevent stray characters.
/// ! Blocks for >240ms.
void DriverControl::set_both_text(const char* text) {
    controller_.clear_line(1);
    pros::delay(60);
    secondary_controller_.clear_line(1);
    pros::delay(60);
    controller_.print(1, 1, text);
    pros::delay(60);
    secondary_controller_.print(1, 1, text);
    pros::delay(60);
}
