#pragma once
// Contains builtin VEX motors and sensors as well as constants.

#include <vector>

#include "control/autonomous_control.hpp"
#include "control/driver_control.hpp"
#include "lemlib/api.hpp"
#include "main.h"
#include "mechanisms/scoring.hpp"

namespace config {
// drivetrain

// ports: negative means reversed
// from robot perspective
inline const std::vector<int8_t> DT_LEFT_PORTS{-14, -15, 16};
inline const std::vector<int8_t> DT_RIGHT_PORTS{11, 12, -13};

// gearset and wheels. use lemlib::Omniwheel namespace, since many wheels'
// names are different from their actual size
constexpr pros::MotorGearset DT_GEARSET{pros::MotorGearset::blue};
constexpr float DT_WHEELS{lemlib::Omniwheel::NEW_325};

// width of the robot, measured from middle of wheels
constexpr float DT_TRACK_WIDTH{13.875};
constexpr float DT_RPM{600};
// lemlib docs:
/* `horizontalDrift` is a feature we added to the original boomerang controller
 * that ensures compatibility with drivetrains with both all omni wheels (drift
 * drive), or drivetrains with center traction wheels. It controls how fast the
 * chassis can move while turning. If you have a drift drive, we recommend
 * starting with a value of 2, while a drivetrain with center traction wheels
 * should start with a value of 8. */
constexpr float DT_HORIZONTAL_DRIFT{8.0};
constexpr float DT_GEAR_RATIO{0.625};

// other motors
constexpr int INTAKE_MOTOR_PORT{-1};
constexpr int TOP_MOTOR_PORT{-3};
constexpr int MIDDLE_MOTOR_PORT{-10};
constexpr int HOPPER_MOTOR_PORT{-2};

// pneumatics
constexpr int LOADER_PORT{'a'};
constexpr bool LOADER_EXTENDED_IS_LOW{false};

constexpr int WING_PORT('b');
constexpr bool WING_EXTENDED_IS_LOW{false};

constexpr int DOUBLE_PARK_PORT('h');
constexpr bool DOUBLE_PARK_EXTENDED_IS_LOW{false};

// odometry
constexpr int IMU_PORT{17};
constexpr int ROTATION_PARALLEL_PORT{8};
constexpr int ROTATION_PERPENDICULAR_PORT{19};
constexpr float TRACKING_WHEELS{lemlib::Omniwheel::NEW_2};

constexpr float PARALLEL_TRACKING_OFFSET{-2.125};  // left is negative
constexpr float PERPENDICULAR_TRACKING_OFFSET{-0.6875};

// other sensors
constexpr int OPTICAL_LEFT_PORT{4};
constexpr int OPTICAL_RIGHT_PORT{18};

// code
constexpr int DRIVE_VELOCITY_PERCENT = 100;
constexpr int TURN_VELOCITY_PERCENT = 70;

// declarations (do not edit)
pros::Controller controller(pros::E_CONTROLLER_MASTER);

// drivetrain
pros::MotorGroup dt_left_motors(DT_LEFT_PORTS, DT_GEARSET);
pros::MotorGroup dt_right_motors(DT_RIGHT_PORTS, DT_GEARSET);

const lemlib::Drivetrain drivetrain(&dt_left_motors, &dt_right_motors,
                                    DT_TRACK_WIDTH, DT_WHEELS, DT_RPM,
                                    DT_HORIZONTAL_DRIFT);

// other motors
pros::Motor intake_motor(INTAKE_MOTOR_PORT);
pros::Motor top_motor(TOP_MOTOR_PORT);
pros::Motor middle_motor(MIDDLE_MOTOR_PORT);
pros::Motor hopper_motor(HOPPER_MOTOR_PORT);

// pneumatics
pros::adi::Pneumatics loader(LOADER_PORT, false, LOADER_EXTENDED_IS_LOW);
pros::adi::Pneumatics wing(WING_PORT, false, WING_EXTENDED_IS_LOW);
pros::adi::Pneumatics double_park(DOUBLE_PARK_PORT, false,
                                  DOUBLE_PARK_EXTENDED_IS_LOW);

// odometry
pros::IMU imu(IMU_PORT);

pros::Rotation parallel_sensor(ROTATION_PARALLEL_PORT);
pros::Rotation perpendicular_sensor(ROTATION_PERPENDICULAR_PORT);

lemlib::TrackingWheel parallel_wheel(&parallel_sensor, TRACKING_WHEELS,
                                     PARALLEL_TRACKING_OFFSET);
lemlib::TrackingWheel perpendicular_wheel(&perpendicular_sensor,
                                          TRACKING_WHEELS,
                                          PERPENDICULAR_TRACKING_OFFSET);

lemlib::OdomSensors odom_sensors(&parallel_wheel, nullptr, &perpendicular_wheel,
                                 nullptr, &imu);

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

lemlib::ControllerSettings angular_controller(
    3,   // proportional gain (kP)
    0,   // integral gain (kI)
    12,  // derivative gain (kD)
    0,   // anti windup
    0,   // small error range, in degrees
    0,   // small error range timeout, in milliseconds
    0,   // large error range, in degrees
    0,   // large error range timeout, in milliseconds
    0    // maximum acceleration (slew)
);

lemlib::Chassis chassis(drivetrain, lateral_controller, angular_controller,
                        odom_sensors);

// other sensors
pros::Optical left_optical(OPTICAL_LEFT_PORT);
pros::Optical right_optical(OPTICAL_RIGHT_PORT);

// code
Scoring scoring(top_motor, middle_motor, intake_motor, hopper_motor,
                left_optical, right_optical);
DriverControl driver_control(chassis, controller, scoring, loader, wing,
                             double_park, DRIVE_VELOCITY_PERCENT,
                             TURN_VELOCITY_PERCENT);
AutonomousControl autonomous_control(chassis, scoring, loader, wing);
}  // namespace config
