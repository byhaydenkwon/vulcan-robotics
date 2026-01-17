#include "autonomous_control.hpp"

#include "lemlib/api.hpp"
#include "main.h"

void AutonomousControl::match_right() {
    chassis_.setPose(0, 0, 0);

    // get three blocks from loader
    chassis_.moveToPose(-10.028, 33.942, 90, 2000, {}, false);
    loader_.extend();
    pros::delay(300);
    chassis_.moveToPoint(10.528, 29.942, 1000, {.maxSpeed = 80.0}, false);
    scoring_.intake();
    pros::delay(700);  // three blocks, most of the time (four if not)

    // move to goal; score four blocks
    chassis_.moveToPoint(-27.72, 31.0, 2000, {.forwards = false}, false);
    scoring_.score(Scoring::ScoreTarget::High);
    scoring_.stop_intaking();
    loader_.retract();
    pros::delay(2000);

    // wing/long goal control sequence
    // wing_.extend();
    // chassis_.moveToPose(-15.0, 13.0, 270, 2300, {}, false);
    // scoring_.stop_scoring(Scoring::ScoreTarget::High);
    // wing_.retract();
    // chassis_.moveToPoint(-45.0, 24.0, 2000,
    //                      {.minSpeed = 80, .earlyExitRange = 7}, false);
    chassis_.moveToPoint(-15.0, 25.0, 2000, {}, false);
    // wing_.retract();

    // get three blocks in middle
    scoring_.intake();
    chassis_.turnToHeading(250, 1000);
    chassis_.moveToPoint(-46.5, -1.0, 2000, {.maxSpeed = 70.0}, false);
    pros::delay(1000);

    // score in low
    scoring_.stop_intaking();
    scoring_.score(Scoring::ScoreTarget::Low);
}

void AutonomousControl::match_left() {
    chassis_.setPose(0, 0, 0);
    chassis_.moveToPose(10.028, 33.942, 270, 2300, {}, false);
    loader_.extend();
    pros::delay(500);
    chassis_.moveToPoint(-8.028, 29.942, 1000, {}, false);
    scoring_.intake();
    pros::delay(700);
    chassis_.moveToPoint(27.72, 31.75, 2000, {.forwards = false}, false);
    scoring_.stop_intaking();
    loader_.retract();
    scoring_.score(Scoring::ScoreTarget::High);
    // chassis_.moveToPoint(23.72, 26, 2000, {.forwards = false}, false);
    // chassis_.moveToPoint(23.72, 32.736756, 2000, {}, false);
    // wing_.extend();
}

void AutonomousControl::skills() {
    // right-side 4 blocks + long goal control auto
    chassis_.setPose(0, 0, 0);
    chassis_.moveToPose(-10.028, 33.942, 90, 2300, {}, false);
    loader_.extend();
    pros::delay(500);
    chassis_.moveToPoint(8.028, 29.942, 1000, {.maxSpeed = 80.0}, false);
    scoring_.intake();
    pros::delay(700);
    chassis_.moveToPoint(-27.72, 31.0, 2000, {.forwards = false}, false);
    scoring_.stop_intaking();
    loader_.retract();
    scoring_.score(Scoring::ScoreTarget::High);
    pros::delay(2500);
    chassis_.moveToPose(-15.0, 14.0, 270, 2300, {}, false);
    scoring_.stop_scoring(Scoring::ScoreTarget::High);
    wing_.extend();
    pros::delay(200);
    wing_.retract();
    chassis_.moveToPoint(-45.0, 25.0, 2300, {}, false);
    chassis_.moveToPoint(-15.0, 25.0, 2300, {.forwards = false}, false);
    wing_.retract();
    // get out any extra blocks in order to ensure control

    // go clear other loader
    // chassis_.moveToPose(float x, float y, float theta, int timeout)
}
