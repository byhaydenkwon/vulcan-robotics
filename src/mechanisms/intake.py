"""
Contains the Intake class.
"""

from vex import *

from display import Logger, NullLogger

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
            "Starting intake + " + ('for ' + str(duration) + 'ms' if duration else 'indefinitely'),
        )

    def stop_intake(self, auto_hopper=True) -> None:
        """
        Stops the intake.
        If auto_hopper is True, this function also stops the hopper.
        """
        self.bottom.stop(HOLD)
        self.logger.log(__name__, "Stopping intake")
        if auto_hopper:
            self.hopper.stop()
