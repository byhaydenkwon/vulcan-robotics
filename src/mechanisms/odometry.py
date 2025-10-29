import math

from vex import *

from utils.display import Logger, NullLogger


class DrivetrainOdometry:
    """
    In the absence of tracking wheels, uses drivetrain motor
    positions to calculate the average linear distance
    traveled by each wheel.

    gear_ratio is the amount of revolutions the drivetrain output has for
    each motor revolution.
    """

    # Please do not implement turns into this.
    # It's probably inaccurate enough as-is.

    def __init__(
        self,
        front_right: Motor,
        middle_right: Motor,
        back_right: Motor,
        front_left: Motor,
        middle_left: Motor,
        back_left: Motor,
        wheel_diameter: float,
        gear_ratio: float = 0.625,
        logger: Logger | NullLogger = NullLogger(),
    ):
        self.drivetrain = {
            "back_right": back_right,
            "back_left": back_left,
            "middle_right": middle_right,
            "middle_left": middle_left,
            "front_right": front_right,
            "front_left": front_left,
        }

        self.gear_ratio = gear_ratio
        self.diameter = wheel_diameter
        self.logger = logger

    def reset_tracking(self) -> None:
        """
        Resets tracking values.
        """
        for motor in self.drivetrain.values():
            motor.reset_position()
        self.logger.log(__name__, "Drivetrain odometry reset")

    def get_distance_traveled(self) -> float:
        """
        Returns distance traveled by drivetrain wheels.
        """
        avg_revolutions = sum(
            [motor.position(TURNS) for motor in self.drivetrain.values()]
        ) / len(self.drivetrain)
        return abs(avg_revolutions * self.gear_ratio * self.diameter * math.pi)
