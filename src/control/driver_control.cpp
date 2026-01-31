#include "driver_control.hpp"

#include <atomic>
#include <memory>

#include "lemlib/api.hpp"
#include "main.h"
#include "mechanisms/scoring.hpp"

void DriverControl::detect_controllers() {
    pros::delay(300);  // for controller printing text
    if (controller_.is_connected() && !secondary_controller_.is_connected()) {
        controller_.print(1, 1, "one controller");
        use_two_controllers_ = false;
    } else {
        controller_.print(1, 1, "two controllers");
    }

    if (use_two_controllers_) {
        active_mechanism_control_ =
            &DriverControl::two_controller_mechanism_control;
    } else {
        active_mechanism_control_ =
            &DriverControl::one_controller_mechanism_control;
    }
}

void DriverControl::start_control_loop() {
    pros::Task driver_control_task([this] -> void { this->control_loop(); },
                                   TASK_PRIORITY_DEFAULT,
                                   TASK_STACK_DEPTH_DEFAULT, "driver control");

    if (use_two_controllers_) {
        // start the controller feedback task at default - 1 priority
        pros::Task controller_feedback_task(
            [this] -> void { this->controllers_feedback_loop(); },
            TASK_PRIORITY_DEFAULT - 1, TASK_STACK_DEPTH_DEFAULT,
            "controller feedback");
    }
}

void DriverControl::control_loop() {
    while (true) {
        split_arcade_drive(drive_velocity_, turn_velocity_);
        // single or dual mechanism control
        (this->*active_mechanism_control_)();
        pros::delay(10);
    }
}

void DriverControl::split_arcade_drive(int drive_velocity,   // NOLINT
                                       int turn_velocity) {  // NOLINT
    int drive_command{controller_.get_analog(pros::E_CONTROLLER_ANALOG_LEFT_Y) *
                      drive_velocity / 100};
    int turn_command{controller_.get_analog(pros::E_CONTROLLER_ANALOG_RIGHT_X) *
                     turn_velocity / 100};

    chassis_.arcade(drive_command, turn_command, true);
}

void DriverControl::two_controller_mechanism_control() {
    // secondary controller

    // secondary set middle score
    if (secondary_controller_.get_digital_new_press(
            pros::E_CONTROLLER_DIGITAL_DOWN)) {
        scoring_middle_ = true;
        scoring_.change_requests(Scoring::ScoreTarget::High,
                                 Scoring::ScoreTarget::Middle);
        set_controllers_text("SCORE MID");
    }

    if (secondary_controller_.get_digital_new_press(
            pros::E_CONTROLLER_DIGITAL_UP)) {
        scoring_middle_ = false;
        scoring_.change_requests(Scoring::ScoreTarget::Middle,
                                 Scoring::ScoreTarget::High);
        set_controllers_text("SCORE HIGH");
    }

    // secondary set intake flushing
    if (secondary_controller_.get_digital_new_press(
            pros::E_CONTROLLER_DIGITAL_X)) {
        intake_flushing_ = true;
        scoring_.change_requests(Scoring::IntakeTarget::Intake,
                                 Scoring::IntakeTarget::Flush);
        set_controllers_text("INTAKE FLUSH");
    }

    if (secondary_controller_.get_digital_new_press(
            pros::E_CONTROLLER_DIGITAL_B)) {
        intake_flushing_ = false;
        scoring_.change_requests(Scoring::IntakeTarget::Flush,
                                 Scoring::IntakeTarget::Intake);
        set_controllers_text("INTAKE NORMAL");
    }

    // primary controller

    // low scoring
    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_R2))
        scoring_.score(Scoring::ScoreTarget::Low);
    else if (controller_.get_digital_new_release(pros::E_CONTROLLER_DIGITAL_R2))
        scoring_.stop_scoring(Scoring::ScoreTarget::Low);

    // L1/L2 scoring logic based on secondary status
    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_L2) ||
        controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_L1)) {
        if (scoring_middle_) {
            scoring_.score(Scoring::ScoreTarget::Middle);
        } else {
            scoring_.score(Scoring::ScoreTarget::High);
        }

    } else if (controller_.get_digital_new_release(
                   pros::E_CONTROLLER_DIGITAL_L2) ||
               controller_.get_digital_new_release(
                   pros::E_CONTROLLER_DIGITAL_L1)) {
        if (scoring_middle_) {
            scoring_.stop_scoring(Scoring::ScoreTarget::Middle);
        } else {
            scoring_.stop_scoring(Scoring::ScoreTarget::High);
        }
    }

    // R1 intake logic based on secondary status
    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_R1)) {
        if (intake_flushing_) {
            scoring_.intake(Scoring::IntakeTarget::Flush);
        } else {
            scoring_.intake(Scoring::IntakeTarget::Intake);
        }
    } else if (controller_.get_digital_new_release(
                   pros::E_CONTROLLER_DIGITAL_R1)) {
        if (intake_flushing_) {
            scoring_.stop_intaking(Scoring::IntakeTarget::Flush);
        } else {
            scoring_.stop_intaking(Scoring::IntakeTarget::Intake);
        }
    }

    // pneumatics
    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_A))
        loader_.toggle();

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_X))
        wing_.toggle();

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_DOWN)) {
        double left_hue = left_optical_.get_hue();
        double right_hue = right_optical_.get_hue();
        int left_prox = left_optical_.get_proximity();
        int right_prox = right_optical_.get_proximity();

        controller_.print(1, 1, "%d", left_prox);
    }
}

void DriverControl::one_controller_mechanism_control() {
    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_R1))
        scoring_.intake(Scoring::IntakeTarget::Intake);
    else if (controller_.get_digital_new_release(pros::E_CONTROLLER_DIGITAL_R1))
        scoring_.stop_intaking(Scoring::IntakeTarget::Intake);

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_R2))
        scoring_.score(Scoring::ScoreTarget::Low);
    else if (controller_.get_digital_new_release(pros::E_CONTROLLER_DIGITAL_R2))
        scoring_.stop_scoring(Scoring::ScoreTarget::Low);

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_L2))
        scoring_.score(Scoring::ScoreTarget::Middle);
    else if (controller_.get_digital_new_release(pros::E_CONTROLLER_DIGITAL_L2))
        scoring_.stop_scoring(Scoring::ScoreTarget::Middle);

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_L1))
        scoring_.score(Scoring::ScoreTarget::High);
    else if (controller_.get_digital_new_release(pros::E_CONTROLLER_DIGITAL_L1))
        scoring_.stop_scoring(Scoring::ScoreTarget::High);

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_A))
        loader_.toggle();

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_X))
        wing_.toggle();

    if (controller_.get_digital_new_press(pros::E_CONTROLLER_DIGITAL_DOWN)) {
        double left_hue = left_optical_.get_hue();
        double right_hue = right_optical_.get_hue();
        int left_prox = left_optical_.get_proximity();
        int right_prox = right_optical_.get_proximity();

        controller_.print(1, 1, "%d", left_prox);
    }
}

void DriverControl::controllers_feedback_loop() {
    std::shared_ptr<const std::string> last_controller_text{nullptr};
    while (true) {
        auto current_controller_text{
            controllers_text_.load(std::memory_order_acquire)};

        if (current_controller_text &&
            current_controller_text != last_controller_text) {
            // actually print the text here, delaying 60ms due to very slow
            // controller text updates
            // lines are cleared to clear stray characters
            controller_.clear_line(1);
            pros::delay(60);
            secondary_controller_.clear_line(1);
            pros::delay(60);
            controller_.print(1, 1, (*current_controller_text).c_str());
            pros::delay(60);
            secondary_controller_.print(1, 1,
                                        (*current_controller_text).c_str());
            pros::delay(60);

            last_controller_text = current_controller_text;
        }

        pros::delay(30);
    }
}

/// Queue text to be set on both controllers.
/// This will replace text currently in the position.
void DriverControl::set_controllers_text(std::string text) {
    controllers_text_.store(std::make_shared<const std::string>(text),
                            std::memory_order_release);
}

void DriverControl::align_double_park_block() {
    double left_hue = left_optical_.get_hue();
    double right_hue = right_optical_.get_hue();
    int left_prox = left_optical_.get_proximity();
    int right_prox = right_optical_.get_proximity();

    controller_.print(1, 1, "%f", left_hue);
    // blue range: 7 closest, 215 farthest
    // red range: 10 closest, 0 farthest
    // left prox no block: 10-25ish
    // prox: either one above 50 means there's a block

    // scoring_.score(Scoring::ScoreTarget::Low);

    // block detected?
    if (!(left_prox > 50 || left_prox < 50)) {
        return;
    }

    // if either hue is [215, 340], it's blue
    // if either hue is [350, 30], it's red
    bool left_hue_blue{left_hue > 215 && left_hue < 340 && left_prox > 110};
    bool left_hue_red{left_hue > 350 || left_hue < 30 && left_prox > 110};

    bool right_hue_blue{right_hue > 215 && right_hue < 340 && right_prox > 110};
    bool right_hue_red{right_hue > 350 || right_hue < 30 && right_prox > 110};

    if (left_hue_blue || right_hue_blue) {
    }
}
