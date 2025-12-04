// The scoring mechanism.
#include <array>

#include "lemlib/api.hpp"
#include "main.h"

// A stack-based intake control class.
class Scoring {
   public:
    enum class ScoreTarget { Low, Middle, High, Count };

    Scoring(pros::Motor top_motor, pros::Motor middle_motor,
            pros::Motor intake_motor, pros::Motor hopper_motor)
        : top_{top_motor},
          middle_{middle_motor},
          intake_{intake_motor},
          hopper_{hopper_motor} {
        active_state_list_.reserve(static_cast<int>(State::Count));
    }

    void intake() { pushActiveState(State::Intaking); }
    void flush() { pushActiveState(State::Flushing); }
    void score(ScoreTarget target) {
        pushActiveState(getStateForScoreTarget(target));
    }

    void stopIntaking() { removeAllStates(State::Intaking); }
    void stopFlushing() { removeAllStates(State::Flushing); }
    void stopScoring(ScoreTarget target) {
        removeAllStates(getStateForScoreTarget(target));
    }

   private:
    enum class State {
        Intaking,
        ScoringLow,
        ScoringMiddle,
        ScoringHigh,
        Flushing,
        Count
    };

    State getStateForScoreTarget(ScoreTarget target) {
        return target_states[static_cast<int>(target)];
    }

    void pushActiveState(State state) {
        state_list_mutex_.take(200);
        active_state_list_.push_back(state);
        state_list_mutex_.give();
    }

    void removeAllStates(State state) {
        state_list_mutex_.take(200);
        active_state_list_.erase(std::remove(active_state_list_.begin(),
                                             active_state_list_.end(), state),
                                 active_state_list_.end());
        state_list_mutex_.give();
    }

    static constexpr std::array<State, static_cast<int>(ScoreTarget::Count)>
        target_states{State::ScoringLow, State::ScoringMiddle,
                      State::ScoringHigh};

    void control_loop() {}

    void spin_score_intake() {}
    void spin_score_flush() {}
    void spin_score_low() {}
    void spin_score_middle() {}
    void spin_score_high() {}

    pros::Motor top_;
    pros::Motor middle_;
    pros::Motor intake_;
    pros::Motor hopper_;

    std::vector<State> active_state_list_{};  // reserved to state count
    pros::Mutex state_list_mutex_;
    bool stop_next_{false};
};
