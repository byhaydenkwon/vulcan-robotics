"""
Contains the AutonomousControl class for autonomous and pre-autonomous code.
"""

from vex import *

from display import Logger, NullLogger


class AutonomousControl:
    """
    Main autonomous control class.
    Contains entry functions for pre-autonomous and autonomous code.
    """

    def __init__(self, logger: Logger | NullLogger = NullLogger()):
        self.logger = logger

    def pre(self) -> None:
        self.logger.log(__name__, "Starting pre-autonomous code")
        # gps_sensor.calibrate()
        # while gps_sensor.is_calibrating():
        #     brain.screen.clear_screen()
        #     brain.screen.print("GPS sensor calibrating")
        #     wait(100, TimeUnits.MSEC)

        # inertial_sensor.calibrate()
        # while gps_sensor.is_calibrating():
        #     brain.screen.clear_screen()
        #     brain.screen.print("Inertial sensor calibrating")
        #     wait(100, TimeUnits.MSEC)

        # optical_sensor.set_light(100)

        pass
        # TODO Have a way to recalibrate after a field adjustment or similar
        # Right now you can just restart the code
        # TODO have a set starting position for the GPS sensor

    def main(self) -> None:
        self.logger.log(__name__, "Starting main autonomous code")
