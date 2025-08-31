from vex import *
import urandom  # type: ignore

import config
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
    setup()

    hopper = Hopper(config.hopper, config.HOPPER_DEGREES_PER_BLOCK)
    intake = Intake(
        config.intake_bottom, config.intake_top, hopper, config.controller_1
    )

    driver = DriverControl(
        "split_arcade", "standard", config.controller_1, intake, hopper
    )
    auto = AutonomousControl()

    comp = Competition(driver.start_control_loop, auto.main)
    auto.pre()


if __name__ == "__main__":
    main()
