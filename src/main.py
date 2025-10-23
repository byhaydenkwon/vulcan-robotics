"""
The file run on the robot brain directly.
Runs VEXCode pregenerated code and sets up boilerplate.
"""

from vex import *
import urandom  # type: ignore

import utils.config as config

import mechanisms.odometry as odometry
from utils.display import Logger, NullLogger, Selection, SelectionButton, UserInterface
from mechanisms.hopper import Hopper
from mechanisms.intake import Intake
from mechanisms.aligner import GoalAligner
from control.autonomous_control import AutonomousControl
from control.driver_control import DriverControl


def setup() -> None:
    """
    A setup function containing mostly VEXCode generated code.
    """

    # wait for rotation sensor to fully initialize
    wait(30, MSEC)

    # Set random seed
    def initializeRandomSeed() -> None:
        wait(100, MSEC)
        random = (
            config.brain.battery.voltage(MV)
            + config.brain.battery.current(CurrentUnits.AMP) * 100
            + config.brain.timer.system_high_res()
        )
        urandom.seed(int(random))

    initializeRandomSeed()

    # add a small delay to make sure we don't print in the middle of the REPL header
    wait(200, MSEC)
    # clear the console to make sure we don't have the REPL in the console
    print("\033[2J")


def calibrate(logger: Logger | NullLogger) -> None:
    logger.log(__name__, "Calibrating GPS sensor")
    config.gps_sensor.calibrate()

    logger.log(__name__, "Calibrating inertial sensor")
    config.inertial_sensor.calibrate()

    config.optical_sensor.set_light(100)
    # TODO (low-priority) Have a way to recalibrate after a field adjustment or similar
    # Right now you can just restart the code


def main() -> None:
    logger = NullLogger()
    setup()
    calibrate(logger)

    # Subsystems and components

    hopper = Hopper(config.hopper, config.HOPPER_DEGREES_PER_BLOCK, logger=logger)
    intake = Intake(
        config.intake_bottom, config.intake_top, hopper, config.controller_1, logger
    )
    Thread(intake.start_control_loop)
    aligner = GoalAligner(config.aligner_out_port, logger)

    # Control

    driver = DriverControl(
        "split_arcade",
        "standard",
        config.front_right,
        config.middle_right,
        config.back_right,
        config.front_left,
        config.middle_left,
        config.back_left,
        config.controller_1,
        intake,
        hopper,
        aligner,
        logger,
        velocity=100,
        turn_velocity=69.42067,
    )
    tracking = odometry.DrivetrainOdometry(
        front_right=config.front_right,
        middle_right=config.middle_right,
        back_right=config.back_right,
        front_left=config.back_left,
        middle_left=config.middle_left,
        back_left=config.back_left,
        wheel_diameter=3.25,
        logger=logger,
    )
    auto = AutonomousControl(
        front_right=config.front_right,
        middle_right=config.middle_right,
        back_right=config.back_right,
        front_left=config.front_left,
        middle_left=config.middle_left,
        back_left=config.back_left,
        hopper=hopper,
        intake=intake,
        inertial=config.inertial_sensor,
        optical=config.optical_sensor,
        gps=config.gps_sensor,
        block_color=config.block_color_sensor,
        tube_pneumatic=config.henry,
        aligner=aligner,
        tracking=tracking,
        drivetrain_velocity=100,
        turn_velocity=50,
        logger=logger,
    )

    logger.log(__name__, "All subsystems successfully initalized")

    # Selection screens and user interface

    auto_selection = Selection(
        "images/vulcan-selection-screen.png",
        {
            SelectionButton(0, 0, 120, 136): auto.position_1_match_auton,  # 1 Out
            SelectionButton(0, 136, 120, 272): auto.position_2_match_auton,  # 2 Out
            SelectionButton(360, 0, 480, 120): auto.position_3_match_auton,  # 3 Out
            SelectionButton(360, 136, 480, 272): auto.position_4_match_auton,  # 4 Out
            SelectionButton(120, 0, 360, 272): auto.skills_auton,  # Skills
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
            logging_thread = Thread(logger.start_print_loop)
            # start the print loop only after the interface ends

        if callable(interface_result["auto"]):
            interface_result["auto"]()

    def start_driver() -> None:
        auto.exit_autonomous()
        driver.start_control_loop()

    config.brain.screen.pressed(handle_input)

    Competition(start_driver, start_auton)


if __name__ == "__main__":
    main()
