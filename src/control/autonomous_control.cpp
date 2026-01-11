#include "autonomous_control.hpp"

#include "lemlib/api.hpp"
#include "main.h"

void AutonomousControl::match_right() {
    chassis_.setPose(0, 0, 0);
    chassis_.moveToPose(-10.028, 33.942, 90, 2300, {}, false);
    loader_.extend();
    pros::delay(500);
    chassis_.moveToPoint(1.528, 28.942, 1000, {}, false);
    scoring_.intake();
    pros::delay(1500);
    chassis_.moveToPoint(-23.72, 32.73675, 2000, {.forwards = false}, false);
    scoring_.stop_intaking();
    loader_.retract();
    scoring_.score(Scoring::ScoreTarget::High);
    pros::delay(3000);
    chassis_.moveToPoint(-23.72, 26, 2000, {.forwards = false}, false);
    chassis_.moveToPoint(-23.72, 32.736756, 2000, {}, false);
    // wing_.extend();
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
    scoring_.score(Scoring::ScoreTarget::Low);
    chassis_.moveToPoint(0, 10, 2000, {.forwards = true}, false);
    chassis_.moveToPoint(0, -25, 2000, {.forwards = false, .maxSpeed = 50},
                         false);
    chassis_.moveToPoint(0, -100, 10000, {.forwards = false}, false);
}
