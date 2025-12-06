#pragma once

#include "lemlib/api.hpp"
#include "main.h"
#include "scoring.hpp"

class AutonomousControl {
   public:
    AutonomousControl(lemlib::Chassis& chassis, Scoring& scoring,
                      pros::adi::Pneumatics& loader)
        : chassis_(chassis), scoring_(scoring), loader_(loader) {};
    void match_right();
    void match_left();
    void skills();

   private:
    lemlib::Chassis& chassis_;
    Scoring& scoring_;
    pros::adi::Pneumatics& loader_;
};
