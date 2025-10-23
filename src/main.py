"""
The file run on the robot brain directly.
Runs VEXCode pregenerated code and sets up boilerplate.
"""

from vex import *
import urandom  # type: ignore

import utils.config as config

import mechanisms.odometry as odometry
from utils.display import Logger, NullLogger, Selection, SelectionButton
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

    # Subsystems, components, and control
    hopper = Hopper(config.hopper, config.HOPPER_DEGREES_PER_BLOCK, logger=logger)
    intake = Intake(
        config.intake_bottom, config.intake_top, hopper, config.controller_1, logger
    )
    Thread(intake.start_control_loop)
    aligner = GoalAligner(config.aligner_out_port, logger)

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

    # Start selection screen

    selection = Selection(
        config.brain,
        "images/vulcan-selection-screen.png",
        {
            SelectionButton(0, 0, 120, 136): lambda: auto.match_auton(LEFT),  # 1
            SelectionButton(0, 136, 120, 272): lambda: auto.match_auton(RIGHT),  # 2
            SelectionButton(360, 0, 480, 120): lambda: auto.match_auton(RIGHT),  # 3
            SelectionButton(360, 136, 480, 272): lambda: auto.match_auton(LEFT),  # 4
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
            for motor in config.drivetrain_motors:
                motor.set_stopping(HOLD)

            logging_thread = Thread(logger.start_print_loop)
            # start the print loop only after the selection ends

            logger.log(__name__, "Starting autonomous code")
            auton_function()
            Thread(intake.start_control_loop)

    def start_driver() -> None:
        auto.exit_autonomous()
        for motor in config.drivetrain_motors:
            motor.set_stopping(BRAKE)
        driver.start_control_loop()

    config.brain.screen.pressed(get_auton)

    Competition(start_driver, start_auton)


if __name__ == "__main__":
    main()
