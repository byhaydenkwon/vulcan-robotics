#include "autonomous_control.hpp"

#include "lemlib/api.hpp"
#include "main.h"

void AutonomousControl::match_right() {
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
    pros::delay(1500);
    chassis_.moveToPose(-15.0, 14.0, 270, 2300, {}, false);
    scoring_.stop_scoring(Scoring::ScoreTarget::High);
    wing_.extend();
    pros::delay(200);
    wing_.retract();
    chassis_.moveToPoint(-45.0, 24.0, 2300, {}, false);
    chassis_.moveToPose(-15.0, 25.0, 270, 2300, {.forwards = false}, false);
    wing_.retract();
    // scoring_.intake();
    // chassis_.moveToPose()
}

void AutonomousControl::match_left() {
    chassis_.setPose(0, 0, 0);
    chassis_.moveToPose(10.028, 33.942, 270, 2300, {}, false);
    loader_.extend();
    pros::delay(500);
    chassis_.moveToPoint(-3.528, 33.942, 1000, {}, false);
    scoring_.intake();
    pros::delay(1500);
    chassis_.moveToPoint(23.72, 32.73675, 2000, {.forwards = false}, false);
    scoring_.stop_intaking();
    loader_.retract();
    scoring_.score(Scoring::ScoreTarget::High);
    chassis_.moveToPoint(23.72, 26, 2000, {.forwards = false}, false);
    chassis_.moveToPoint(23.72, 32.736756, 2000, {}, false);
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
