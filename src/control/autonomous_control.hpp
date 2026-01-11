#pragma once

#include "lemlib/api.hpp"
#include "main.h"
#include "mechanisms/scoring.hpp"

class AutonomousControl {
   public:
    AutonomousControl(lemlib::Chassis& chassis, Scoring& scoring,
                      pros::adi::Pneumatics& loader,
                      pros::adi::Pneumatics& wing)
        : chassis_(chassis), scoring_(scoring), loader_(loader), wing_{wing} {};
    void match_right();
    void match_left();
    void skills();

   private:
    lemlib::Chassis& chassis_;
    Scoring& scoring_;
    pros::adi::Pneumatics& loader_;
    pros::adi::Pneumatics& wing_;
};
