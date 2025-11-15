"""
The file run on the robot brain directly.
Runs VEXCode pregenerated code and sets up boilerplate.
"""

from vex import *

import urandom  # type: ignore

from utils import config
from utils.display import Logger, NullLogger, Selection, SelectionButton, UserInterface

from mechanisms.scoring import Scoring
from mechanisms.pneumatics import GoalAligner, MatchLoader
from mechanisms.drivetrain import Drivetrain

from control.autonomous_control import AutonomousControl
from control.driver_control import DriverControl


def setup() -> None:
    """
    A setup function containing modified VEXCode-generated code.
    """

    # wait for sensor and system setup
    wait(350, MSEC)

    random = (
        config.brain.battery.voltage(MV)
        + config.brain.battery.current(CurrentUnits.AMP) * 100
        + config.brain.timer.system_high_res()
    )
    urandom.seed(int(random))

    # clear the console to make sure we don't have the REPL in the console
    print("\033[2J")


def calibrate(logger: Logger | NullLogger) -> None:
    logger.log(__name__, "Calibrating inertial sensor")
    config.inertial_sensor.calibrate()


def main() -> None:
    setup()

    logger = NullLogger()
    calibrate(logger)

    # Subsystems, components, and control
    drivetrain = Drivetrain(
        front_right=config.front_right,
        middle_right=config.middle_right,
        back_right=config.back_right,
        front_left=config.front_left,
        middle_left=config.middle_left,
        back_left=config.back_left,
        gear_ratio=0.625,
        wheel_diameter=3.25,
    )
    scoring = Scoring(
        top_motor=config.top_motor,
        middle_motor=config.middle_motor,
        intake_motor=config.intake_motor,
        hopper_motor=config.hopper_motor,
        logger=logger,
    )
    aligner = GoalAligner(
        pneumatic=config.aligner_port,
        internal_extended_bool=False,
        default_extended_status=False,
        logger=logger,
    )
    loader = MatchLoader(
        pneumatic=config.match_loader_port,
        internal_extended_bool=False,
        default_extended_status=False,
        logger=logger,
    )

    Thread(scoring.start_control_loop)

    # Control

    driver = DriverControl(
        drive_mode="split_arcade",
        mechanism_mode="standard",
        drivetrain=drivetrain,
        controller=config.controller,
        scoring=scoring,
        aligner=aligner,
        loader=loader,
        logger=logger,
        velocity=100,
        turn_velocity=69.42067,
    )
    auto = AutonomousControl(
        drivetrain=drivetrain,
        scoring=scoring,
        inertial=config.inertial_sensor,
        loader=loader,
        aligner=aligner,
        logger=logger,
    )

    logger.log(__name__, "All subsystems successfully initalized")

    # Selection screens and user interface

    auto_selection = Selection(
        "images/vulcan-selection-screen.png",
        {
            SelectionButton(0, 0, 120, 136): lambda: auto.match_auton(LEFT),  # 1
            SelectionButton(0, 136, 120, 272): lambda: auto.match_auton(RIGHT),  # 2
            SelectionButton(360, 0, 480, 120): lambda: auto.match_auton(RIGHT),  # 3
            SelectionButton(360, 136, 480, 272): lambda: auto.match_auton(LEFT),  # 4
            SelectionButton(120, 0, 360, 272): lambda: auto.skills_auton(),  # Middle
        },
    )

    win_point_selection = Selection(
        "images/vulcan-wp-selection-screen.png",
        {
            SelectionButton(0, 0, 240, 272): auto.i_do_nothing_replace_me,
            SelectionButton(240, 0, 480, 272): auto.i_do_nothing_replace_me,
        },
    )

    brain_interface = UserInterface(
        config.brain, {"auto": auto_selection, "win_point": win_point_selection}, None
    )

    Thread(brain_interface.start_ui_loop)

    interface_result = brain_interface.get_ui_selection_results()

    def handle_input() -> None:
        nonlocal interface_result
        interface_result = brain_interface.get_ui_selection_results()

    def start_auton() -> None:
        if brain_interface.done:
            Thread(logger.start_print_loop)
            # start the print loop only if the interface ends

        if callable(interface_result["auto"]):
            interface_result["auto"]()

    def start_driver() -> None:
        auto.exit_autonomous()
        for motor in drivetrain.motors:
            motor.set_stopping(BRAKE)
        driver.start_control_loop()

    config.brain.screen.pressed(handle_input)

    Competition(start_driver, start_auton)


if __name__ == "__main__":
    main()
