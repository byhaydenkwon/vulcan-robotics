#pragma once

#include "lemlib/api.hpp"
#include "main.h"
#include "mechanisms/scoring.hpp"

struct AutonomousControlParams {
    lemlib::Chassis& chassis;
    pros::adi::Pneumatics& loader;
    pros::adi::Pneumatics& wing;
    pros::adi::Pneumatics& double_park;

    Scoring& scoring;
};

class AutonomousControl {
   public:
    explicit AutonomousControl(AutonomousControlParams params)
        : chassis_(params.chassis),
          scoring_(params.scoring),
          loader_(params.loader),
          wing_{params.wing},
          double_park_{params.double_park} {};
    void match_right();
    void match_left();
    void skills();

   private:
    lemlib::Chassis& chassis_;
    pros::adi::Pneumatics& loader_;
    pros::adi::Pneumatics& wing_;
    pros::adi::Pneumatics& double_park_;

    Scoring& scoring_;
};
