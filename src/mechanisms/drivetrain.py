"""
The drivetrain.

Not a significant source of sat. fat, trans fat, cholesterol, dietary fiber, vitamin D, calcium, and iron.
"""

import math
from vex import *


class Drivetrain:
    def __init__(
        self,
        front_right: Motor,
        middle_right: Motor,
        back_right: Motor,
        front_left: Motor,
        middle_left: Motor,
        back_left: Motor,
        gear_ratio: float,
        wheel_diameter: float,
    ) -> None:
        self.right = [front_right, middle_right, back_right]
        self.left = [front_left, middle_left, back_left]

        # The order of this list determines the motor starting and stopping order
        self.motors = [
            back_right,
            back_left,
            middle_right,
            middle_left,
            front_right,
            front_left,
        ]

        self.gear_ratio = gear_ratio
        self.diameter = wheel_diameter

    def spin_right_motors(
        self, direction: DirectionType.DirectionType, velocity: float
    ) -> None:
        """
        Set the velocity of the right-side motors and spin them.
        """
        for motor in self.right:
            motor.set_velocity(velocity, PERCENT)
            motor.spin(direction)

    def spin_left_motors(
        self, direction: DirectionType.DirectionType, velocity: float
    ) -> None:
        """
        Set the velocity of the right-side motors and spin them.
        """
        for motor in self.left:
            motor.set_velocity(velocity, PERCENT)
            motor.spin(direction)

    def reset_tracking(self) -> None:
        """
        Resets tracking values.
        """
        for motor in self.motors:
            motor.reset_position()

    def get_distance_traveled(self) -> float:
        """
        Returns distance traveled by drivetrain wheels.
        """
        avg_revolutions = sum([motor.position(TURNS) for motor in self.motors]) / len(
            self.motors
        )
        return abs(avg_revolutions * self.gear_ratio * self.diameter * math.pi)
