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

    def __init__(
        self,
        gps: Gps,
        inertial: Inertial,
        optical: Optical,
        logger: Logger | NullLogger = NullLogger(),
    ):
        self.logger = logger
        self.gps = gps
        self.inertial = inertial
        self.optical = optical

    def pre(self) -> None:
        self.logger.log(__name__, "Starting pre-autonomous code")
        self.logger.log(__name__, "Calibrating GPS sensor")
        self.gps.calibrate()

        self.logger.log(__name__, "Calibrating inertial sensor")
        self.inertial.calibrate()

        self.optical.set_light(100)

        pass
        # TODO Have a way to recalibrate after a field adjustment or similar
        # Right now you can just restart the code
        # TODO have a set starting position for the GPS sensor

    def main(self) -> None:
        self.logger.log(__name__, "Starting main autonomous code")
