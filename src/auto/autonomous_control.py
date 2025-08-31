"""
Contains the AutonomousControl class for autonomous and pre-autonomous code.
"""

from vex import *

import config


class AutonomousControl:
    """
    Main autonomous control class.
    Contains entry functions for pre-autonomous and autonomous code.
    """

    def pre(self) -> None:
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
        config.brain.screen.clear_screen()
        config.brain.screen.print("autonomous code not implemented")
