#pragma once

#include "lemlib/api.hpp"
#include "main.h"
#include "mechanisms/scoring.hpp"
#include "utils/settings.hpp"

class AutonomousControl {
   public:
    AutonomousControl(Settings& settings, lemlib::Chassis& chassis,
                      Scoring& scoring, pros::adi::Pneumatics& loader,
                      pros::adi::Pneumatics& wing)
        : settings_(settings),
          chassis_(chassis),
          scoring_(scoring),
          loader_(loader),
          wing_{wing} {};
    void match_right();
    void match_left();
    void skills();

   private:
    Settings& settings_;
    lemlib::Chassis& chassis_;
    Scoring& scoring_;
    pros::adi::Pneumatics& loader_;
    pros::adi::Pneumatics& wing_;
};
