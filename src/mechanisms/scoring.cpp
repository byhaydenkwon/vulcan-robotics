/// The scoring mechanism.
#include "mechanisms/scoring.hpp"

#include <algorithm>
#include <atomic>
#include <cmath>
#include <ranges>
#include <vector>

#include "lemlib/api.hpp"
#include "main.h"

void Scoring::start_control_loop() {
    pros::Task scoring_task([this] -> void { this->control_loop(); },
                            TASK_PRIORITY_DEFAULT, TASK_STACK_DEPTH_DEFAULT,
                            "intake");
}

auto Scoring::get_state_for_score_target(Scoring::ScoreTarget target)
    -> Scoring::State {
    return score_target_states_[static_cast<int>(target)];
}

auto Scoring::get_state_for_intake_target(Scoring::IntakeTarget target)
    -> Scoring::State {
    return intake_target_states_[static_cast<int>(target)];
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

void Scoring::remove_all_of_state(Scoring::State state) {
    if (state_list_mutex_.take(200)) {
        std::erase(active_state_list_, state);
        state_list_mutex_.give();
    } else {
        printf("STATE LIST MUTEX TIMED OUT WHILE REMOVING STATE");
    }
}

void Scoring::clear_all_states() {
    if (state_list_mutex_.take(200)) {
        active_state_list_.clear();
        state_list_mutex_.give();
    } else {
        printf("STATE LIST MUTEX TIMED OUT WHILE CLEARING STATES");
    }
}

void Scoring::change_states(State of, State to) {
    if (state_list_mutex_.take(200)) {
        std::ranges::replace(active_state_list_, of, to);
        state_list_mutex_.give();
    } else {
        printf("STATE LIST MUTEX TIMED OUT EXCHANGING");
    }
}

auto Scoring::is_state_in_list(State state) -> bool {
    bool result{false};
    if (state_list_mutex_.take(200)) {
        result = std::ranges::contains(active_state_list_, state);
        state_list_mutex_.give();
    } else {
        printf("STATE LIST MUTEX TIMED OUT CHECKING FOR STATE");
    }

    return result;
}

void Scoring::control_loop() {
    while (!stop_next_) {
        State active{State::Idle};

        if (state_list_mutex_.take(200)) {
            if (!active_state_list_.empty()) {
                active = active_state_list_.back();

                // is double parking about to be removed? set
                // double_park_result_
                if (std::ranges::contains(active_state_list_,
                                          State::DoubleParking) &&
                    active != State::DoubleParking) {
                    double_park_state_.store(DoubleParkState::IndefiniteCancel,
                                             std::memory_order_release);
                }

                // remove any finite states if they're in the state list and not
                // the last item
                auto new_end = std::ranges::remove_if(
                    active_state_list_, [active](State state) -> bool {
                        return std::ranges::find(FINITE_STATES, state) !=
                                   FINITE_STATES.end() &&
                               state != active;
                    });

                active_state_list_.erase(new_end.begin(), new_end.end());
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
                spin_score_middle();
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
            case State::DoubleParking:
                spin_double_park();
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
void Scoring::spin_score_high() {
    spin_motor_percent(top_, -100);
    spin_motor_percent(middle_, 100);
    spin_motor_percent(intake_, 100);
    spin_motor_percent(hopper_, -100);
}
void Scoring::spin_score_middle() {
    spin_motor_percent(top_, 80);
    spin_motor_percent(middle_, 100);
    spin_motor_percent(intake_, 100);
    spin_motor_percent(hopper_, -75);
}
void Scoring::spin_score_low() {
    spin_motor_percent(top_, 100);
    spin_motor_percent(middle_, -100);
    spin_motor_percent(intake_, -100);
    spin_motor_percent(hopper_, -100);
}
void Scoring::spin_double_park() {
    int left_prox = left_optical_.get_proximity();
    int right_prox = right_optical_.get_proximity();

    if (left_prox > 50 || right_prox > 50) {  // block detected
        pros::delay(300);                     // ! SORRY
        double_park_state_.store(DoubleParkState::Success,
                                 std::memory_order_release);
        spin_stop();
        remove_all_of_state(State::DoubleParking);
    } else {
        spin_motor_percent(top_, 70);
        spin_motor_percent(middle_, -70);
        spin_motor_percent(intake_, -70);
        spin_motor_percent(hopper_, -70);
    }

    // * Keeping hue comment information here for now,
    // * because I don't have anywhere else I would reasonably remember this

    // double left_hue = left_optical_.get_hue();
    // double right_hue = right_optical_.get_hue();

    // blue range: 7 closest, 215 farthest
    // red range: 10 closest, 0 farthest
    // if either hue is [215, 340], it's blue
    // if either hue is [350, 30], it's red
}

/// Spin a `pros::Motor` based on percentage of max velocity, rounded up to
/// the nearest RPM.
void Scoring::spin_motor_percent(const pros::Motor& motor, float percent) {
    int max_rpm;
    const pros::MotorGears gearset{motor.get_gearing()};

    // Motor gearset values are hardcoded. If these change, we have bigger
    // problems.
    // Or you could just switch these numbers.
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
