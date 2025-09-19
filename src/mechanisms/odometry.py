import math

from vex import *

from display import Logger, NullLogger

# TODO make planar and absolute odometry, make a base class for odometry and inherit


class LinearOdometry:
    """
    One-dimensional simple odometry for calculating
    straight distance traveled with a single parallel tracking wheel.
    """

    def __init__(
        self,
        encoder: Rotation,
        wheel_diameter: float,
        logger: Logger | NullLogger = NullLogger(),
    ) -> None:
        self._encoder = encoder
        self.diameter = wheel_diameter
        self.logger = logger

    def reset_tracking(self) -> None:
        self._encoder.reset_position()
        self.logger.log(__name__, "1D position tracking reset")

    def get_distance_traveled(self) -> float:
        """
        Returns relative distance traveled in the direction of the tracking wheel.
        """
        return self.diameter * math.pi * self._encoder.position(RotationUnits.REV)
