#include "autonomous_control.hpp"

#include "lemlib/api.hpp"
#include "main.h"

void AutonomousControl::right_awp() {
    // 1. go to loader, grab 3 blocks
    // 2. score 4 in long goal
    // 3. get 3 close center blocks
    // 4. score them in low
    // 5. get 3 far center blocks
    // 6. score them in high

    // get three blocks from loader
    chassis_.moveToPose(-10.428, 34.342, 90, 2000, {}, false);
    loader_.extend();
    pros::delay(300);
    chassis_.moveToPoint(10.528, 29.942, 1000, {.maxSpeed = 73.5}, false);
    scoring_.intake(Scoring::IntakeTarget::Intake);
    pros::delay(700);  // three blocks, most of the time (four if not)

    // move to goal; score four blocks
    chassis_.moveToPoint(-28.12, 30.2, 2000, {.forwards = false}, true);
    chassis_.waitUntil(13.);
    scoring_.score(Scoring::ScoreTarget::High);
    scoring_.stop_intaking(Scoring::IntakeTarget::Intake);
    loader_.retract();
    chassis_.waitUntilDone();
    pros::delay(1300);
    scoring_.stop_scoring(Scoring::ScoreTarget::High);

    // pick up close three center blocks
    chassis_.moveToPoint(-20, 30.2, 1000, {}, false);
    chassis_.moveToPose(-24, 16.8, 235, 1500, {}, false);
    scoring_.intake();

    // score in low
    chassis_.moveToPose(-44, 3.5, 235, 3000, {.maxSpeed = 70}, true);
    chassis_.waitUntil(8.);
    scoring_.stop_intaking();
    scoring_.score(Scoring::ScoreTarget::Low);
}

void AutonomousControl::right_together() {
    // eventually, this should:
    // 1. go to center and get 3 center blocks
    // 2. score 4 blocks in lower goal
    // 3. go to loader and load 3 blocks
    // 4. score 3 blocks in long goal
    // 5. wing those 3 blocks to get control of long goal

    chassis_.setPose(0, 0, 0);

    // get three blocks from loader
    chassis_.moveToPose(-10.428, 34.342, 90, 2000, {}, false);
    loader_.extend();
    pros::delay(300);
    chassis_.moveToPoint(10.528, 29.942, 1000, {.maxSpeed = 73.5}, false);
    scoring_.intake(Scoring::IntakeTarget::Intake);
    pros::delay(700);  // three blocks, most of the time (four if not)

    // move to goal; score four blocks
    chassis_.moveToPoint(-28.12, 30.2, 2000, {.forwards = false}, false);
    scoring_.score(Scoring::ScoreTarget::High);
    scoring_.stop_intaking(Scoring::IntakeTarget::Intake);
    loader_.retract();
    pros::delay(2000);
    scoring_.stop_scoring(Scoring::ScoreTarget::High);

    // wing / long goal control sequence (only)
    wing_.extend();
    chassis_.moveToPose(-15.0, 14.0, 270, 2300, {}, false);
    wing_.retract();

    // the following for winging and moving back
    // chassis_.moveToPoint(-52.0, 25.0, 2000,
    //                      {.minSpeed = 80, .earlyExitRange = 7}, false);
    // chassis_.moveToPoint(-15.0, 25.0, 2000, {.forwards = false}, false);
    // wing_.retract();

    chassis_.moveToPoint(-45.0, 25.5, 2000, {}, false);
    wing_.extend();
    scoring_.intake();
    chassis_.moveToPose(-40.0, 6.0, 235, 5000, {.maxSpeed = 100}, false);
}

void AutonomousControl::left_together() {
    // eventually, this should:
    // 1. go to center and get 3 center blocks
    // 2. score 4 blocks in upper center goal
    // 3. go to loader and load 3 blocks
    // 4. score 3 blocks in long goal
    // 5. wing those 3 blocks to get control of long goal

    chassis_.setPose(0, 0, 0);
    chassis_.moveToPose(10.028, 33.942, 270, 2300, {}, false);
    loader_.extend();
    pros::delay(500);
    chassis_.moveToPoint(-8.028, 29.942, 1000, {}, false);
    scoring_.intake(Scoring::IntakeTarget::Intake);
    pros::delay(700);
    chassis_.moveToPoint(27.72, 31.75, 2000, {.forwards = false}, false);
    scoring_.stop_intaking(Scoring::IntakeTarget::Intake);
    loader_.retract();
    scoring_.score(Scoring::ScoreTarget::High);
    // chassis_.moveToPoint(23.72, 26, 2000, {.forwards = false}, false);
    // chassis_.moveToPoint(23.72, 32.736756, 2000, {}, false);
    // wing_.extend();
}

void AutonomousControl::skills() {
    // eventually, this should:
    // 1. go to right-side loader and clear
    // 2. go to other side of field (same long goal); score six blocks there
    // 3. move backward and clear loader
    // 4. score six blocks on same long goal
    // 5. move to other side (different long goal) and clear loader
    // 6. move to other side (same long goal as 5.) and score
    // 7. clear loader and score blocks
    // 8. park

    chassis_.setPose(0, 0, 0);

    // get six blocks from loader
    chassis_.moveToPose(-10.428, 34.342, 90, 2000, {}, false);
    loader_.extend();
    pros::delay(300);
    chassis_.moveToPoint(10.528, 29.942, 1000, {.maxSpeed = 73.5}, false);
    scoring_.intake();
    pros::delay(1300);

    // go to other side of field
    chassis_.moveToPoint(-10, 47, 4000, {}, false);
    scoring_.stop_intaking();
    loader_.retract();
    chassis_.moveToPoint(-110, 51, 10000, {}, false);

    // move to high goal and score
    chassis_.moveToPose(-92.5, 33.5, 270, 3000, {.forwards = false}, false);
    scoring_.score(Scoring::ScoreTarget::High);
    pros::delay(2000);
    scoring_.stop_scoring(Scoring::ScoreTarget::High);

    // get six blocks from loader
    loader_.extend();
    scoring_.intake();
    chassis_.moveToPose(-121.403, 34.0, 270, 2000, {}, false);
    pros::delay(1300);

    // move to high goal and score
    chassis_.moveToPose(-92.5, 33.5, 270, 2000, {.forwards = false}, false);
    scoring_.stop_intaking();
    scoring_.score(Scoring::ScoreTarget::High);
    pros::delay(2000);
    scoring_.stop_scoring(Scoring::ScoreTarget::High);
}

void AutonomousControl::sixty_s_stop_time() { double_park_.extend(); }
