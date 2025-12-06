/// The scoring mechanism.
#include "scoring.hpp"

#include <cmath>
#include <ranges>
#include <vector>

#include "lemlib/api.hpp"
#include "main.h"

void Scoring::start_control_loop() {
    pros::Task scoring_task([this] { this->control_loop(); },
                            TASK_PRIORITY_DEFAULT, TASK_STACK_DEPTH_DEFAULT,
                            "intake");
}

Scoring::State Scoring::get_state_for_score_target(
    Scoring::ScoreTarget target) {
    return target_states_[static_cast<int>(target)];
}

void Scoring::push_active_state(Scoring::State state) {
    // * we don't risk stopping the entire robot
    if (state_list_mutex_.take(200)) {
        if (!std::ranges::contains(active_state_list_, state)) {
            active_state_list_.push_back(state);
        }
        state_list_mutex_.give();
    } else {
        printf("STATE LIST MUTEX TIMED OUT WHILE PUSHING STATE\n");
    }
}

void Scoring::remove_all_states(Scoring::State state) {
    if (state_list_mutex_.take(200)) {
        std::erase(active_state_list_, state);
        state_list_mutex_.give();
    } else {
        printf("STATE LIST MUTEX TIMED OUT WHILE REMOVING STATE");
    }
}

void Scoring::control_loop() {
    while (!stop_next_) {
        State active{State::Idle};

        if (state_list_mutex_.take(200)) {
            if (!active_state_list_.empty()) {
                active = active_state_list_.back();
            }
            state_list_mutex_.give();
        } else {
            printf("STATE LIST MUTEX TIMED OUT IN CONTROL LOOP");
        }

        switch (active) {
            case State::Intaking:
                spin_intake();
                break;
            case State::Flushing:
                spin_flush();
                break;
            case State::ScoringLow:
                spin_score_low();
                break;
            case State::ScoringMiddle:
                spin_score_middle();
                break;
            case State::ScoringHigh:
                spin_score_high();
                break;
            default:
                spin_stop();
        }

        pros::Task::delay(25);
    }
}

void Scoring::spin_stop() {
    top_.brake();
    middle_.brake();
    intake_.brake();
    hopper_.brake();
}
void Scoring::spin_intake() {
    top_.brake();
    spin_motor_percent(middle_, 100);
    spin_motor_percent(intake_, 100);
    spin_motor_percent(hopper_, 100);
}
void Scoring::spin_flush() {
    spin_motor_percent(top_, 100);
    spin_motor_percent(middle_, 100);
    spin_motor_percent(intake_, 100);
    spin_motor_percent(hopper_, -100);
}
void Scoring::spin_score_high() {
    spin_motor_percent(top_, -100);
    spin_motor_percent(middle_, 100);
    intake_.brake();
    spin_motor_percent(hopper_, -100);
}
void Scoring::spin_score_middle() {
    spin_motor_percent(top_, 100);
    spin_motor_percent(middle_, 100);
    intake_.brake();
    spin_motor_percent(hopper_, -100);
}
void Scoring::spin_score_low() {
    spin_motor_percent(top_, 100);
    spin_motor_percent(middle_, -100);
    spin_motor_percent(intake_, -100);
    spin_motor_percent(hopper_, -100);
}

/// Spin a `pros::Motor` based on percentage of max velocity, rounded up to
/// the nearest RPM.
void Scoring::spin_motor_percent(const pros::Motor& motor, float percent) {
    int max_rpm;
    const pros::MotorGears gearset{motor.get_gearing()};

    switch (gearset) {
        case pros::MotorGears::ratio_36_to_1:
            max_rpm = 100;
            break;
        case pros::MotorGears::ratio_18_to_1:
            max_rpm = 200;
            break;
        case pros::MotorGears::ratio_6_to_1:
            max_rpm = 600;
            break;
        default:
            max_rpm = 200;
    }

    motor.move_velocity(std::ceil((percent / 100.0) * max_rpm));
}
