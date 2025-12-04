#pragma once
// Contains builtin VEX motors and sensors as well as constants.

#include <vector>

#include "lemlib/api.hpp"
#include "main.h"
namespace config {
// drivetrain

// ports: negative means reversed
inline const std::vector<int> DT_RIGHT_PORTS{-14, -15, 16};
inline const std::vector<int> DT_LEFT_PORTS{11, 12, -13};

// gearset and wheels. use lemlib::Omniwheel namespace, since many wheels'
// names are different from their actual size
constexpr pros::MotorGearset DT_GEARSET{pros::MotorGearset::blue};
constexpr float DT_WHEELS{lemlib::Omniwheel::NEW_325};

// width of the robot, measured from middle of wheels
constexpr float DT_TRACK_WIDTH{13.875};
constexpr float DT_RPM{600};
constexpr float DT_HORIZONTAL_DRIFT{2.0};
constexpr float DT_GEAR_RATIO{0.625};

// other motors
constexpr int INTAKE_MOTOR_PORT{-1};
constexpr int TOP_MOTOR_PORT{-3};
constexpr int MIDDLE_MOTOR_PORT{-10};
constexpr int HOPPER_MOTOR_PORT{-2};
constexpr int ALIGNER_PORT{'a'};
constexpr int LOADER_PORT{'b'};

// sensors
constexpr int IMU_PORT{17};
constexpr int ROTATION_PARALLEL_PORT{-9};
constexpr int ROTATION_PERPENDICULAR_PORT{20};

// odometry
constexpr float PARALLEL_TRACKING_OFFSET{-2.125};  // left is negative
constexpr float PERPENDICULAR_TRACKING_OFFSET{-0.6875};

}  // namespace config
