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

    void set_controllers_text(std::string text);

    bool use_two_controllers_{true};
    void (DriverControl::*active_mechanism_control_)(){
        &DriverControl::two_controller_mechanism_control};

    int drive_velocity_{100};
    int turn_velocity_{75};

    bool scoring_middle_{false};
    bool intake_flushing_{false};

    // these variables are used to store the status of scoring_middle_
    // and intake_flushing at the time of activation; so that even if
    // the secondary controller switches the mode for either;
    // the release still stops the correct action.
    bool last_scoring_middle_{scoring_middle_};
    bool last_intake_flushing_{intake_flushing_};

    // controller text setting publishes to this pointer
    std::atomic<std::shared_ptr<const std::string>> controllers_text_{nullptr};

    lemlib::Chassis& chassis_;
    pros::Controller& controller_;
    pros::Controller& secondary_controller_;

    Scoring& scoring_;
    pros::adi::Pneumatics& loader_;
    pros::adi::Pneumatics& wing_;
    pros::adi::Pneumatics& double_park_;
};
