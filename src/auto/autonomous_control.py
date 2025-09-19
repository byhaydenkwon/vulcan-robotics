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

        self.motors = [
            front_right,
            middle_right,
            back_right,
            front_left,
            middle_left,
            back_left,
        ]

        self.right_motors = self.motors[:3]
        self.left_motors = self.motors[3:]

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

        self.drive(FORWARD, 4.0, 100, True)
        # drive forward 4 inches at 100% velocity and wait for completion

        self.drive(REVERSE, 10.0, 60, False)
        # drive reverse 10 inches at 60% velocity and don't wait for completion

        self.turn(50, RIGHT, 50)
        # turn right 50 degrees at 50% velocity

        pass

    def position_2_match_auton(self) -> None:
        pass

    def position_3_match_auton(self) -> None:
        # self.intake.start_intake(100)
        # self.drive(FORWARD, 10, 60, True)
        self.turn(20, RIGHT, 60)
        # self.drive(FORWARD, 15, 45, False)

    def position_4_match_auton(self) -> None:
        pass

    def drive(
        self,
        direction: DirectionType.DirectionType,
        distance: float,
        velocity: int | None,
        wait=True,
    ) -> None:
        # NOTE: For now, just make sure you use the same units for
        # distance and wheel diameter.
        # Should add different units and better positional tracking later.

        self.middle_right.set_position(0, TURNS)
        travel_rotations = distance / (self.wheel_diameter * math.pi * 2)
        for motor in self.motors:
            motor.set_velocity(
                velocity if velocity is not None else self.drivetrain_velocity, PERCENT
            )
            motor.spin(FORWARD, velocity, PERCENT)

        while self.middle_right.position(TURNS) < travel_rotations:
            pass

        def stop_left() -> None:
            for motor in self.left_motors:
                motor.stop()

        def stop_right() -> None:
            for motor in self.right_motors:
                motor.stop()

        Thread(stop_left)
        Thread(stop_right)

        # if wait:
        #     self.logger.log(__name__, "WAITING")
        #     for motor in self.motors:
        #         while not motor.is_done():
        #             pass

    def turn(
        self, degrees: float, direction: TurnType.TurnType, velocity: int | None
    ) -> None:
        # NOTE Relies on the inertial sensor for now.
        # this is just a bit bad (it's bad)

        if direction == TurnType.UNDEFINED:
            return

        initial_heading = self.inertial.heading()

        turn_target = (
            (initial_heading - degrees)
            if direction == TurnType.LEFT
            else (initial_heading + degrees)
        )
        # This could need to be reversed, with left positive and right negative.

        acceptable_turn_difference = (
            turn_target - turn_target * 0.025,
            turn_target + turn_target * 0.025,
        )
        # Allow for x% of error.
        # This does mean that if it's not detected the first time, it will
        # make a 360 degree rotation before trying again.

        if direction == TurnType.RIGHT:
            turn_motors = [self.left_motors, self.right_motors.reverse]
        else:
            turn_motors = [self.right_motors, self.left_motors.reverse]

        # turn_motors = (
        # self.left_motors if direction == TurnType.LEFT else self.right_motors
        # )

        for motor in turn_motors:
            motor.spin(FORWARD, velocity, PERCENT)

        while (
            self.inertial.heading() < acceptable_turn_difference[0]
            or self.inertial.heading() > acceptable_turn_difference[1]
        ):  # outside of acceptable range
            pass
            # This isn't the best since there's no escape hatch
            # TODO fix later (along with everything here tbh)

        # for motor in turn_motors:
        # motor.stop()

    @staticmethod
    def i_do_nothing_replace_me(*args, **kwargs) -> None:
        """
        Do nothing.
        Dummy autonomous code function.
        """
        pass
