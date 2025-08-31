from vex import *

from hopper import Hopper


class Intake:
    def __init__(
        self,
        bottom_motor: Motor,
        top_motor: Motor,
        hopper: Hopper,
        controller: Controller,
    ) -> None:
        self.bottom = bottom_motor
        self.top = top_motor
        self.hopper = hopper
        self.controller = controller

    def start_intake(
        self, velocity: int, duration: int | None = None, auto_hopper=True
    ) -> None:
        """
        Starts the intake for the specified duration in milliseconds.
        Runs indefinitely if no duration is provided.
        Velocity must be provided as a percentage.

        If auto_hopper is True, this function also starts the hopper.
        """
        self.bottom.set_velocity(velocity, PERCENT)
        if auto_hopper:
            self.hopper.intake()
        if duration:
            timer = Timer()
            timer.event(self.stop_intake, duration)

    def stop_intake(self, auto_hopper=True) -> None:
        """
        Stops the intake.
        If auto_hopper is True, this function also stops the hopper.
        """
        self.bottom.set_velocity(0, PERCENT)
        if auto_hopper:
            self.hopper.stop()
