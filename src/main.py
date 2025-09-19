"""
The file run on the robot brain directly.
Runs VEXCode pregenerated code and sets up boilerplate.
"""

from vex import *
import urandom  # type: ignore

import config

from display import Logger, Selection, SelectionButton
from mechanisms.hopper import Hopper
from mechanisms.intake import Intake
from auto.autonomous_control import AutonomousControl
from driver.driver_control import DriverControl


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


def main() -> None:
    # TODO: clean this up and move it all out of main

    setup()

    logger = Logger(config.brain)

    # Calibration

    logger.log(__name__, "Calibrating GPS sensor")
    config.gps_sensor.calibrate()

    logger.log(__name__, "Calibrating inertial sensor")
    config.inertial_sensor.calibrate()

    config.optical_sensor.set_light(100)

    # TODO Have a way to recalibrate after a field adjustment or similar
    # Right now you can just restart the code
    # TODO have a set starting position for the GPS sensor

    # Subsystems and components

    hopper = Hopper(config.hopper, config.HOPPER_DEGREES_PER_BLOCK, logger=logger)
    intake = Intake(
        config.intake_bottom, config.intake_top, hopper, config.controller_1, logger
    )

    driver = DriverControl(
        "split_arcade",
        "standard",
        config.controller_1,
        intake,
        hopper,
        logger,
        velocity=100,
        turn_velocity=69.42067,
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
        tracking_mode=None,
        drivetrain_velocity=100,
        turn_velocity=50,
        wheel_diameter=3.25,
        logger=logger,
    )

    logger.log(__name__, "All subsystems successfully initalized")

    selection = Selection(
        config.brain,
        "images/vulcan-selection-screen.png",
        {
            SelectionButton(0, 0, 120, 136): auto.position_1_match_auton,  # 1 Out
            SelectionButton(0, 136, 120, 272): auto.position_2_match_auton,  # 2 Out
            SelectionButton(360, 0, 480, 120): auto.position_3_match_auton,  # 3 Out
            SelectionButton(360, 136, 480, 272): auto.position_4_match_auton,  # 4 Out
        },
    )

    auton_function: Callable | None = None

    def get_auton() -> None:
        nonlocal auton_function
        auton_function = selection.pressed()
        if auton_function is not None:
            config.brain.screen.clear_screen(Color.GREEN)

    def start_auton() -> None:
        if auton_function is not None:
            logging_thread = Thread(logger.start_print_loop)
            # start the print loop only after the selection ends

            logger.log(__name__, "Starting autonomous code")
            auton_function()

    config.brain.screen.pressed(get_auton)

    Competition(driver.start_control_loop, start_auton)


if __name__ == "__main__":
    main()
