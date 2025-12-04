#include "main.h"

#include "config.hpp"
#include "lemlib/chassis/chassis.hpp"
#include "lemlib/chassis/trackingWheel.hpp"
#include "pros/rotation.hpp"

pros::Controller controller(pros::E_CONTROLLER_MASTER);

pros::MotorGroup left_motors({-14, -15, 16}, pros::MotorGearset::ratio_6_to_1);
pros::MotorGroup right_motors({11, 12, -13}, pros::MotorGearset::ratio_6_to_1);

const lemlib::Drivetrain drivetrain(&left_motors, &right_motors, 13.875,
                                    lemlib::Omniwheel::NEW_325, 600, 2);

pros::Imu imu(17);

pros::Rotation parallel_sensor(-9);
pros::Rotation perpendicular_sensor(20);

lemlib::TrackingWheel parallel_wheel(&parallel_sensor, lemlib::Omniwheel::NEW_2,
                                     -2.125);
lemlib::TrackingWheel perpendicular_wheel(&perpendicular_sensor,
                                          lemlib::Omniwheel::NEW_2, -0.6875);

lemlib::OdomSensors sensors(&parallel_wheel, nullptr, &perpendicular_wheel,
                            nullptr, &imu);

// lateral PID controller
lemlib::ControllerSettings lateral_controller(
    10,   // proportional gain (kP)
    0,    // integral gain (kI)
    3,    // derivative gain (kD)
    3,    // anti windup
    1,    // small error range, in inches
    100,  // small error range timeout, in milliseconds
    3,    // large error range, in inches
    500,  // large error range timeout, in milliseconds
    20    // maximum acceleration (slew)
);

// angular PID controller
lemlib::ControllerSettings angular_controller(
    2,    // proportional gain (kP)
    0,    // integral gain (kI)
    10,   // derivative gain (kD)
    3,    // anti windup
    1,    // small error range, in degrees
    100,  // small error range timeout, in milliseconds
    3,    // large error range, in degrees
    500,  // large error range timeout, in milliseconds
    0     // maximum acceleration (slew)
);

lemlib::Chassis chassis(drivetrain, lateral_controller, angular_controller,
                        sensors);

/**
 * Runs initialization code. This occurs as soon as the program is started.
 *
 * All other competition modes are blocked by initialize; it is recommended
 * to keep execution time for this mode under a few seconds.
 */
void initialize() {
    pros::lcd::initialize();  // initialize brain screen
    chassis.calibrate();
}

/**
 * Runs while the robot is in the disabled state of Field Management System or
 * the VEX Competition Switch, following either autonomous or opcontrol. When
 * the robot is enabled, this task will exit.
 */
void disabled() {}

/**
 * Runs after initialize(), and before autonomous when connected to the Field
 * Management System or the VEX Competition Switch. This is intended for
 * competition-specific initialization routines, such as an autonomous selector
 * on the LCD.
 *
 * This task will exit when the robot is enabled and autonomous or opcontrol
 * starts.
 */
void competition_initialize() {}

/**
 * Runs the user autonomous code. This function will be started in its own task
 * with the default priority and stack size whenever the robot is enabled via
 * the Field Management System or the VEX Competition Switch in the autonomous
 * mode. Alternatively, this function may be called in initialize or opcontrol
 * for non-competition testing purposes.
 *
 * If the robot is disabled or communications is lost, the autonomous task
 * will be stopped. Re-enabling the robot will restart the task, not re-start it
 * from where it left off.
 */
void autonomous() {
    chassis.setPose(0, 0, 0);

    chassis.turnToHeading(90, 1000000);
}

/**
 * Runs the operator control code. This function will be started in its own task
 * with the default priority and stack size whenever the robot is enabled via
 * the Field Management System or the VEX Competition Switch in the operator
 * control mode.
 *
 * If no competition control is connected, this function will run immediately
 * following initialize().
 *
 * If the robot is disabled or communications is lost, the
 * operator control task will be stopped. Re-enabling the robot will restart the
 * task, not resume it from where it left off.
 */
void opcontrol() {
    while (true) {
        int y_input = controller.get_analog(pros::E_CONTROLLER_ANALOG_LEFT_Y);
        int x_input = controller.get_analog(pros::E_CONTROLLER_ANALOG_RIGHT_X);

        chassis.arcade(y_input, x_input, true);

        pros::delay(20);
    }
}
