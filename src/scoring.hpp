#pragma once

#include <array>

#include "lemlib/api.hpp"
#include "main.h"

/// A stack-based intake control class.
class Scoring {
   public:
    enum class ScoreTarget { Low, Middle, High, InvalidCount };

    Scoring(pros::Motor top_motor, pros::Motor middle_motor,
            pros::Motor intake_motor, pros::Motor hopper_motor)
        : top_{top_motor},
          middle_{middle_motor},
          intake_{intake_motor},
          hopper_{hopper_motor} {
        active_state_list_.reserve(static_cast<int>(State::InvalidCount));
    }

    void start_control_loop();
    void stop_control_loop() { stop_next_ = true; }

    void intake() { push_active_state(State::Intaking); }
    void flush() { push_active_state(State::Flushing); }
    void score(ScoreTarget target) {
        push_active_state(get_state_for_score_target(target));
    }

    void stop_intaking() { remove_all_states(State::Intaking); }
    void stop_flushing() { remove_all_states(State::Flushing); }
    void stop_scoring(ScoreTarget target) {
        remove_all_states(get_state_for_score_target(target));
    }

   private:
    enum class State {
        Idle,
        Intaking,
        ScoringLow,
        ScoringMiddle,
        ScoringHigh,
        Flushing,
        InvalidCount
    };

    State get_state_for_score_target(ScoreTarget target);

    static constexpr std::array<State,
                                static_cast<int>(ScoreTarget::InvalidCount)>
        target_states_{State::ScoringLow, State::ScoringMiddle,
                       State::ScoringHigh};

    void push_active_state(State state);
    void remove_all_states(State state);

    void control_loop();

    void spin_stop();
    void spin_intake();
    void spin_flush();
    void spin_score_high();
    void spin_score_middle();
    void spin_score_low();

    static void spin_motor_percent(const pros::Motor& motor, float percent);

    pros::Motor top_;
    pros::Motor middle_;
    pros::Motor intake_;
    pros::Motor hopper_;

    // technically not a stack, but close!
    // elements are removed from the middle of the list
    std::vector<State> active_state_list_{};  // reserved to state count
    pros::Mutex state_list_mutex_;
    bool stop_next_{false};
};
