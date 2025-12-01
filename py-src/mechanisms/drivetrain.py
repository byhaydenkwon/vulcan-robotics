"""
The drivetrain.

Not a significant source of sat. fat, trans fat, cholesterol, dietary fiber, vitamin D, calcium, and iron.
"""

import math

from vex import *


class Drivetrain:
    def __init__(
        self,
        right_1: Motor,
        right_2: Motor,
        right_3: Motor,
        left_1: Motor,
        left_2: Motor,
        left_3: Motor,
        gear_ratio: float,
        wheel_diameter: float,
    ) -> None:
        self.right = [right_1, right_2, right_3]
        self.left = [left_1, left_2, left_3]

        # The order of this list determines the motor starting and stopping order
        self.motors = [
            right_3,
            left_3,
            right_2,
            left_2,
            right_1,
            left_1,
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

    def spin_motors(
        self, direction: DirectionType.DirectionType, velocity: float
    ) -> None:
        """
        Set the velocity of all motors and spin them.
        """
        for motor in self.motors:
            motor.set_velocity(velocity, PERCENT)
            motor.spin(direction)

    def stop_motors(self) -> None:
        """
        Stop all motors.
        """
        for motor in self.motors:
            motor.stop()

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
