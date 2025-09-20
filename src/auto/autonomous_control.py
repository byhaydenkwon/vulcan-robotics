"""
Contains the AutonomousControl class for autonomous code.
"""

import math

from vex import *

from display import Logger, NullLogger
from mechanisms.hopper import Hopper
from mechanisms.intake import Intake


class AutonomousControl:
    """
    Contains autonomous code helper functions.
    """

    def __init__(
        self,
        front_right: Motor,
        middle_right: Motor,
        back_right: Motor,
        front_left: Motor,
        middle_left: Motor,
        back_left: Motor,
        hopper: Hopper,
        intake: Intake,
        inertial: Inertial,
        optical: Optical,
        gps: Gps,
        block_color: Optical,
        tube_pneumatic: DigitalOut,
        tracking_mode: str | None,
        drivetrain_velocity: int,
        turn_velocity: int,
        wheel_diameter: float,
        logger: Logger | NullLogger = NullLogger(),
    ):
        self.front_right = front_right
        self.middle_right = middle_right
        self.back_right = back_right
        self.front_left = front_left
        self.middle_left = middle_left
        self.back_left = back_left

        # The order of this list determines the motor stopping order
        self.drivetrain = [
            back_right,
            back_left,
            middle_right,
            middle_left,
            front_right,
            front_left,
        ]

        self.right_drivetrain = self.drivetrain[:3]
        self.left_drivetrain = self.drivetrain[3:]

        self.hopper = hopper
        self.intake = intake
        self.inertial = inertial
        self.optical = optical
        self.gps = gps
        self.block_color = block_color
        self.tube_pneumatic = tube_pneumatic

        self.tracking_mode = tracking_mode

        self.drivetrain_velocity = drivetrain_velocity
        self.turn_velocity = turn_velocity
        self.wheel_diameter = wheel_diameter

        self.logger = logger

    def position_1_match_auton(self) -> None:
        # Code here. Sorry I didn't have time to add it!
        # NOTE At idle-ish points, try to sleep(5) here and there
        # to allow time for other threads to execute. This will only slow the routine
        # down by 1/200th of a second.

        # Move forward, intake, move back to realign, then forward and turn twice to score
        # EXAMPLE DRIVE FUNCTIONS

        self.drive(FORWARD, 4.0, 100)
        # drive forward 4 inches at 100% velocity and wait for completion

        self.drive(REVERSE, 10.0, 60)
        # drive reverse 10 inches at 60% velocity and don't wait for completion

        self.pivot_turn(50, RIGHT, 50)
        # turn right 50 degrees at 50% velocity

        pass

    def position_2_match_auton(self) -> None:
        pass

    def position_3_match_auton(self) -> None:
        # self.intake.start_intake(100)
        pass

    def position_4_match_auton(self) -> None:
        pass

    def drive(
        self,
        direction: DirectionType.DirectionType,
        distance: float,
        velocity: int | None,
    ) -> None:
        # NOTE: For now, just make sure you use the same units for
        # distance and wheel diameter.
        # Should add different units and better positional tracking later.

        # Use middle right wheel as tracking wheel.
        self.middle_right.set_position(0, TURNS)
        travel_rotations = distance / (self.wheel_diameter * math.pi * 2)
        for motor in self.drivetrain:
            motor.set_velocity(
                velocity if velocity is not None else self.drivetrain_velocity, PERCENT
            )
            motor.spin(direction, velocity, PERCENT)

        while self.middle_right.position(TURNS) < travel_rotations:
            pass

        for motor in self.drivetrain:
            motor.stop()

    def pivot_turn(
        self, degrees: float, direction: TurnType.TurnType, velocity: int | None
    ) -> None:
        """
        Autonomously turn in place using all wheels.
        """
        # NOTE Relies on the inertial sensor for now.

        if direction == TurnType.UNDEFINED:
            return

        self.inertial.reset_heading()

        turn_target = -degrees if direction == TurnType.LEFT else degrees
        acceptable_turn_difference = (
            turn_target - turn_target * 0.025,
            turn_target + turn_target * 0.025,
        )
        # Allow for x% of error.
        # This does mean that if it's not detected the first time, it will
        # make a 360 degree rotation before trying to stop again.

        forward_motors = (
            self.right_drivetrain
            if direction == TurnType.LEFT
            else self.left_drivetrain
        )

        for motor in self.drivetrain:
            motor.spin(
                FORWARD if motor in forward_motors else REVERSE, velocity, PERCENT
            )

        while (
            self.inertial.heading() < acceptable_turn_difference[0]
            or self.inertial.heading() > acceptable_turn_difference[1]
        ):  # outside of acceptable range
            pass

        for motor in self.drivetrain:
            motor.stop()

    @staticmethod
    def i_do_nothing_replace_me(*args, **kwargs) -> None:
        """
        Do nothing.
        Dummy autonomous code function.
        """
        pass
