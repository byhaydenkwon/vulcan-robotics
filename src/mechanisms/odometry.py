import math

from vex import *

from utils.display import Logger, NullLogger


class DrivetrainOdometry:
    """
    In the absence of tracking wheels, uses drivetrain motor
    positions to calculate the average linear distance
    traveled by each wheel.
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
        logger: Logger | NullLogger = NullLogger(),
    ):
        self.front_right = front_right
        self.middle_right = middle_right
        self.back_right = back_right
        self.front_left = front_left
        self.middle_left = middle_left
        self.back_left = back_left

        self.drivetrain = {
            "back_right": back_right,
            "back_left": back_left,
            "middle_right": middle_right,
            "middle_left": middle_left,
            "front_right": front_right,
            "front_left": front_left,
        }

        self.diameter = wheel_diameter

        self.logger = logger

        self._next_stop_tracking = False

        # {"back_right": 0.0, "back_left": 0.0, ...}
        self.revolutions = {name: 0.0 for name in self.drivetrain.keys()}
        self.previous_revolutions = {name: 0.0 for name in self.drivetrain.keys()}

    def reset_tracking(self) -> None:
        """
        Resets tracking.
        """
        self.revolutions = {name: 0.0 for name in self.drivetrain.keys()}

        for motor in self.drivetrain.values():
            motor.reset_position()

        self.revolutions = {name: 0.0 for name in self.drivetrain.keys()}
        self.previous_revolutions = {name: 0.0 for name in self.drivetrain.keys()}

        self.logger.log(__name__, "Drivetrain odometry reset")

    def start_tracking(self, direction: DirectionType.DirectionType) -> None:
        """
        Starts tracking. If not reset, continues tracking.
        """
        self.logger.log(__name__, "Drivetrain odometry started")
        while not self._next_stop_tracking:
            for name, motor in self.drivetrain.items():
                pos = motor.position(TURNS)

                # get forward distance between old and new positions, wrapping around 1
                # ex. (0.5 - 0.4) % 1 = 0.1 % 1 = 0.1
                # (0.1 - 0.9) % 1 = -0.8 % 1 = 0.2
                # note: floating-point inaccuracies may lead to a
                # rounding error of about 10E-16
                if direction == FORWARD:
                    self.revolutions[name] += (
                        pos - self.previous_revolutions[name]
                    ) % 1
                else:
                    self.revolutions[name] += (
                        self.previous_revolutions[name] - pos
                    ) % 1

                self.previous_revolutions[name] = pos
            sleep(20)
        self.logger.log(__name__, "Drivetrain odometry stopped")

    def stop_tracking(self) -> None:
        self._next_stop_tracking = True

    def get_distance_traveled(self) -> float:
        avg_revolutions = sum(self.revolutions.values()) / len(self.revolutions)
        # gear ratio is 1:1.6 driven:driver
        return avg_revolutions * 0.6 * self.diameter * math.pi


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
        self.logger.log(__name__, "Linear odometry (re-)started")

    def start_tracking(self, direction) -> None:
        self.logger.log(__name__, "Linear odometry started")

    def stop_tracking(self, *args, **kwargs) -> None:
        self.logger.log(__name__, "Linear odometry stopped")

    def get_distance_traveled(self) -> float:
        """
        Returns relative distance traveled in the direction of the tracking wheel.
        """
        return self.diameter * math.pi * self._encoder.position(RotationUnits.REV)
