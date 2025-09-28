"""
Contains the Intake class.
"""

from vex import *

from utils.display import Logger, NullLogger

from mechanisms.hopper import Hopper


class Intake:
    def __init__(
        self,
        bottom_motor: Motor,
        top_motor: Motor,
        hopper: Hopper,
        controller: Controller,
        logger: Logger | NullLogger = NullLogger(),
    ) -> None:
        self.bottom = bottom_motor
        self.top = top_motor
        self.hopper = hopper
        self.controller = controller
        self.logger = logger

    def start_intake(
        self, velocity: int, duration: int | None = None, auto_hopper=True
    ) -> None:
        """
        Starts the intake for the specified duration in milliseconds.
        Runs indefinitely if no duration is provided.
        Velocity must be provided as a percentage.

        If auto_hopper is True, this function also starts the hopper.
        """
        self.bottom.spin(FORWARD, velocity, PERCENT)
        if auto_hopper:
            self.hopper.intake()
        if duration:
            timer = Timer()
            timer.event(self.stop_intake, duration)

        self.logger.log(
            __name__,
            "Starting intake + "
            + ("for " + str(duration) + "ms" if duration else "indefinitely"),
        )

    def stop_intake(self, auto_hopper=True) -> None:
        """
        Stops the intake.
        If auto_hopper is True, this function also stops the hopper.
        """
        self.bottom.stop()
        self.top.stop()

        self.logger.log(__name__, "Stopping intake")
        if auto_hopper:
            self.hopper.stop()

    def output_bottom_goal(
        self, velocity: int, duration: int | None = None, auto_hopper=True
    ) -> None:
        """
        Outputs blocks to the bottom goal with an optional time and velocity.
        """
        self.stop_intake()

        self.bottom.spin(REVERSE, velocity, PERCENT)
        if auto_hopper:
            self.hopper.flush()
        if duration:
            timer = Timer()
            timer.event(self.stop_intake, duration)

        self.logger.log(
            __name__,
            "Intake output bottom + "
            + ("for " + str(duration) + "ms" if duration else "indefinitely"),
        )

    def output_middle_goal(
        self, velocity: int, duration: int | None = None, auto_hopper=True
    ) -> None:
        """
        Outputs blocks to the middle goal with an optional time and velocity.
        """
        self.stop_intake()

        self.bottom.spin(FORWARD, velocity, PERCENT)
        self.top.spin(FORWARD, velocity, PERCENT)

        if auto_hopper:
            self.hopper.flush()
        if duration:
            timer = Timer()
            timer.event(self.stop_intake, duration)

        self.logger.log(
            __name__,
            "Intake output middle + "
            + ("for " + str(duration) + "ms" if duration else "indefinitely"),
        )

    def output_top_goal(
        self, velocity: int, duration: int | None = None, auto_hopper=True
    ) -> None:
        """
        Outputs blocks to the top goal with an optional time and velocity.
        """
        self.stop_intake()

        self.bottom.spin(FORWARD, velocity, PERCENT)
        self.top.spin(REVERSE, velocity, PERCENT)

        if auto_hopper:
            self.hopper.flush()
        if duration:
            timer = Timer()
            timer.event(self.stop_intake, duration)

        self.logger.log(
            __name__,
            "Intake output top + "
            + ("for " + str(duration) + "ms" if duration else "indefinitely"),
        )
