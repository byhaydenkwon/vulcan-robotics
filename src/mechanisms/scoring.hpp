#pragma once

#include <array>
#include <atomic>

#include "lemlib/api.hpp"
#include "main.h"

struct ScoringParams {
    pros::Motor& top_motor;
    pros::Motor& middle_motor;
    pros::Motor& intake_motor;
    pros::Motor& hopper_motor;

    pros::Optical& left_optical;
    pros::Optical& right_optical;
};

/// A stack-based intake control class.
class Scoring {
   public:
    explicit Scoring(ScoringParams params)
        : top_{params.top_motor},
          middle_{params.middle_motor},
          intake_{params.intake_motor},
          hopper_{params.hopper_motor},
          left_optical_{params.left_optical},
          right_optical_{params.right_optical} {
        active_state_list_.reserve(static_cast<int>(State::InvalidCount));
    }

    enum class IntakeTarget { Intake, Flush, InvalidCount };
    enum class ScoreTarget { Low, Middle, High, InvalidCount };
    enum class ColorSorting { None, Red, Blue, InvalidCount };
    enum class DoubleParkState {
        Attempting,
        Success,
        ExternalCancel,
        IndefiniteCancel,
        InvalidCount
    };

    void start_control_loop();
    void stop_control_loop() { stop_next_ = true; }

    void intake(IntakeTarget target = IntakeTarget::Intake) {
        push_active_state(get_state_for_intake_target(target));
    }
    void score(ScoreTarget target) {
        push_active_state(get_state_for_score_target(target));
    }
    /// Requests a finite scoring state, which means this will stop
    /// automatically when the sensor detects the double park is complete.
    void double_park() {
        push_active_state(State::DoubleParking);
        double_park_state_ = DoubleParkState::Attempting;
    }

    void stop_intaking(IntakeTarget target) {
        remove_all_of_state(get_state_for_intake_target(target));
    }
    void stop_scoring(ScoreTarget target) {
        remove_all_of_state(get_state_for_score_target(target));
    }
    void stop_double_parking() {
        remove_all_of_state(State::DoubleParking);
        double_park_state_ = DoubleParkState::ExternalCancel;
    }

    auto double_park_state() -> DoubleParkState {
        return double_park_state_.load(std::memory_order_acquire);
    }

    void change_requests(ScoreTarget of, ScoreTarget to) {
        change_states(get_state_for_score_target(of),
                      get_state_for_score_target(to));
    }
    void change_requests(IntakeTarget of, IntakeTarget to) {
        change_states(get_state_for_intake_target(of),
                      get_state_for_intake_target(to));
    }

    void stop_all() { clear_all_states(); }

    ColorSorting color_sorting_mode_{ColorSorting::None};

   private:
    enum class State {
        Idle,
        Intaking,
        Flushing,
        ScoringLow,
        ScoringMiddle,
        ScoringHigh,
        DoubleParking,
        InvalidCount
    };

    // Semantically, these states are *behaviors*, and private functions
    // implement those behaviors. It is somewhat imprecise, because most of
    // these states are *indefinite* while one (double park) is finite, but I
    // don't think *enforcing* a strict separate-enum split based on this
    // specifically is necessary for this codebase, if only because the
    // implementation would be very nearly the same. Even now, the functions
    // which really only need to be called once are called continuously until
    // cancelled. If you wish to fix or expand this later, I would probably
    // split Scoring::State into IndefiniteState and FiniteState or something
    // like that, and then adjust the behavior of Scoring::control_loop() as
    // necessary (storing the past value, not calling if the same, whatever).

    // For now, what I'll do is simply store a list of the indefinite states and
    // make sure they get removed from the control loop if they exist and
    // they're not at the top of the state list. This will be the simplest
    // acceptable solution.

    //
    static constexpr std::array<State, 1> FINITE_STATES{State::DoubleParking};

    auto get_state_for_score_target(ScoreTarget target) -> State;
    auto get_state_for_intake_target(IntakeTarget target) -> State;

    static constexpr std::array<State,
                                static_cast<int>(ScoreTarget::InvalidCount)>
        score_target_states_{State::ScoringLow, State::ScoringMiddle,
                             State::ScoringHigh};

    static constexpr std::array<State,
                                static_cast<int>(IntakeTarget::InvalidCount)>
        intake_target_states_{State::Intaking, State::Flushing};

    void push_active_state(State state);
    void remove_all_of_state(State state);
    void clear_all_states();
    void change_states(State of, State to);
    auto is_state_in_list(State state) -> bool;

    void control_loop();

    void spin_stop();
    void spin_intake();
    void spin_score_high();
    void spin_score_middle();
    void spin_score_low();
    void spin_double_park();

    static void spin_motor_percent(const pros::Motor& motor, float percent);

    std::atomic<DoubleParkState> double_park_state_{
        DoubleParkState::InvalidCount};

    pros::Motor& top_;
    pros::Motor& middle_;
    pros::Motor& intake_;
    pros::Motor& hopper_;
    pros::Optical& left_optical_;
    pros::Optical& right_optical_;

    // technically not a stack, but close!
    // elements are removed from the middle of the list
    std::vector<State> active_state_list_{};  // reserved to state count
    pros::Mutex state_list_mutex_;

    bool stop_next_{false};
};
