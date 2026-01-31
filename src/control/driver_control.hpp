#pragma once

#include <memory>

#include "lemlib/api.hpp"
#include "main.h"
#include "mechanisms/scoring.hpp"

struct DriverControlParams {
    lemlib::Chassis& chassis;
    pros::Controller& controller;
    pros::Controller& secondary_controller;
    pros::adi::Pneumatics& loader;
    pros::adi::Pneumatics& wing;
    pros::adi::Pneumatics& double_park;

    pros::Optical& left_optical;
    pros::Optical& right_optical;

    Scoring& scoring;

    int drive_velocity;
    int turn_velocity;
    bool use_two_controllers;
};

// ? It may be better later to refactor this into two classes, one of which
// ? inherits and morphs the mechanism control function.

/// Driver control class.
class DriverControl {
   public:
    explicit DriverControl(DriverControlParams params)
        : chassis_{params.chassis},
          controller_{params.controller},
          secondary_controller_{params.secondary_controller},
          scoring_{params.scoring},
          loader_{params.loader},
          left_optical_{params.left_optical},
          right_optical_{params.right_optical},
          double_park_{params.double_park},
          wing_{params.wing},
          drive_velocity_{params.drive_velocity},
          turn_velocity_{params.turn_velocity},
          use_two_controllers_{params.use_two_controllers} {}

    void start_control_loop();
    void detect_controllers();

   private:
    void control_loop();
    void controllers_feedback_loop();

    void split_arcade_drive(int drive_velocity, int turn_velocity);
    void two_controller_mechanism_control();
    void one_controller_mechanism_control();

    void align_double_park_block();
    void set_controllers_text(std::string text);

    bool use_two_controllers_{true};
    void (DriverControl::*active_mechanism_control_)(){
        &DriverControl::two_controller_mechanism_control};

    int drive_velocity_{100};
    int turn_velocity_{75};

    bool scoring_middle_{false};
    bool intake_flushing_{false};

    // controller text setting publishes to this pointer
    std::atomic<std::shared_ptr<const std::string>> controllers_text_{nullptr};

    lemlib::Chassis& chassis_;
    pros::Controller& controller_;
    pros::Controller& secondary_controller_;

    pros::Optical& left_optical_;
    pros::Optical& right_optical_;

    Scoring& scoring_;
    pros::adi::Pneumatics& loader_;
    pros::adi::Pneumatics& wing_;
    pros::adi::Pneumatics& double_park_;
};
