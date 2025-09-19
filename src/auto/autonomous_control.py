"""
Contains the AutonomousControl class for autonomous code.
"""

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
            back_left,
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
        # down by 1/200th of a second.abs
        pass

    def position_2_match_auton(self) -> None:
        # Code here. Sorry I didn't have time to add it!
        # NOTE At idle-ish points, try to sleep(5) here and there
        # to allow time for other threads to execute. This will only slow the routine
        # down by 1/200th of a second.abs
        pass

    def position_3_match_auton(self) -> None:
        # Code here. Sorry I didn't have time to add it!
        # NOTE At idle-ish points, try to sleep(5) here and there
        # to allow time for other threads to execute. This will only slow the routine
        # down by 1/200th of a second.abs
        pass

    def position_4_match_auton(self) -> None:
        # Code here. Sorry I didn't have time to add it!
        # NOTE At idle-ish points, try to sleep(5) here and there
        # to allow time for other threads to execute. This will only slow the routine
        # down by 1/200th of a second.abs
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
        travel_rotations = distance / self.wheel_diameter
        for motor in self.motors:
            motor.spin_for(
                direction=direction,
                rot_or_time=travel_rotations,
                units=RotationUnits.REV,
                velocity=velocity,
                wait=wait,
            )

    def turn(self, degrees: float, direction: TurnType, velocity: int | None) -> None:
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

        turn_motors = (
            self.left_motors if direction == TurnType.LEFT else self.right_motors
        )

        for motor in turn_motors:
            motor.spin(
                FORWARD,
                velocity if velocity is not None else self.turn_velocity,
                PERCENT,
            )

        while (
            self.inertial.heading() < acceptable_turn_difference[0]
            or self.inertial.heading() > acceptable_turn_difference[1]
        ):  # outside of acceptable range
            pass
            # This isn't the best since there's no escape hatch
            # TODO fix later (along with everything here tbh)

        for motor in turn_motors:
            motor.stop()

    @staticmethod
    def i_do_nothing_replace_me(*args, **kwargs) -> None:
        """
        Do nothing.
        Dummy autonomous code function.
        """
        pass
