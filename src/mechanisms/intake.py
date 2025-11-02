"""
Contains the Intake class.
"""

from vex import *

from utils.enums import IntakeStates, IntakeStateValue, IntakeTargets, IntakeTargetValue
from utils.display import Logger, NullLogger


class Intake:
    """
    A stack-based intake control class.
    """

    def __init__(
        self,
        bottom_motor: Motor,
        top_motor: Motor,
        hopper_motor: Motor,
        logger: Logger | NullLogger = NullLogger(),
    ) -> None:
        self.bottom = bottom_motor
        self.top = top_motor
        self.hopper = hopper_motor
        self.logger = logger

        self.target_states: dict[IntakeTargetValue, IntakeStateValue] = {
            IntakeTargets.INTAKE: IntakeStates.INTAKING,
            IntakeTargets.LOW: IntakeStates.OUTTAKING_LOW,
            IntakeTargets.MIDDLE: IntakeStates.OUTTAKING_MIDDLE,
            IntakeTargets.HIGH: IntakeStates.OUTTAKING_HIGH,
        }

        # Okay, technically not a stack. Last in is not always first out.
        # But close enough.
        self.stack: list[IntakeStateValue] = []

        self._next_stop_control = False

    def start_control_loop(self) -> None:
        """
        Starts the intake stack control loop.
        """
        while not self._next_stop_control:
            if not self.stack:
                active = IntakeStates.OFF
            else:
                try:
                    active = self.stack[-1]
                except IndexError:
                    from utils import config

                    config.brain.screen.clear_screen(Color.RED)
                    # if the error is fixed ever

            if active == IntakeStates.OFF:
                self.bottom.stop()
                self.top.stop()
                self.hopper.stop()
            elif active == IntakeStates.INTAKING:
                self.bottom.spin(FORWARD, 100, PERCENT)
                self.top.stop()
                self.hopper.spin(FORWARD, 100, PERCENT)
            elif active == IntakeStates.OUTTAKING_LOW:
                self.bottom.spin(REVERSE, 100, PERCENT)
                self.top.stop()
                self.hopper.spin(REVERSE, 100, PERCENT)
            elif active == IntakeStates.OUTTAKING_MIDDLE:
                self.bottom.spin(FORWARD, 100, PERCENT)
                self.top.spin(FORWARD, 100, PERCENT)
                self.hopper.spin(REVERSE, 100, PERCENT)
            elif active == IntakeStates.OUTTAKING_HIGH:
                self.bottom.spin(FORWARD, 100, PERCENT)
                self.top.spin(REVERSE, 100, PERCENT)
                self.hopper.spin(REVERSE, 100, PERCENT)
            if len(self.stack) > 4:
                self.stack = self.stack[4:]
                # this prevents issues when the buttons are spammed extremely quickly

            wait(15, MSEC)

    def stop_control_loop(self) -> None:
        """
        Stops the intake control loop.
        """
        self._next_stop_control = True

    def start_intake(self, duration: int | None = None) -> None:
        """
        Starts the intake for the specified duration in milliseconds.
        Runs indefinitely if no duration is provided.
        """

        if IntakeStates.INTAKING not in self.stack:
            self.stack.append(IntakeStates.INTAKING)

        if duration:
            timer = Timer()
            timer.event(lambda: self.stop_command(IntakeTargets.INTAKE), duration)

        self.logger.log(
            __name__,
            "Starting intake + "
            + ("for " + str(duration) + "ms" if duration else "indefinitely"),
        )

    def output(self, target: IntakeTargetValue, duration: int | None = None):
        """
        Outputs the intake at the specified level for a duration in milliseconds.
        Runs indefinitely if no duration is provided.
        """
        try:
            new_state = self.target_states[target]
        except KeyError:
            self.logger.log(__name__, "PROVIDED OUTPUT TARGET NOT IN STATES")
            return

        if new_state not in self.stack:
            self.stack.append(new_state)

        if duration:
            timer = Timer()
            timer.event(lambda: self.stop_command(new_state), duration)
        self.logger.log(
            __name__,
            new_state + ("for " + str(duration) + "ms" if duration else "indefinitely"),
        )

    def stop_command(self, stop: IntakeTargetValue) -> None:
        """
        Removes all IntakeStates of the passed IntakeTarget from the command stack.
        """
        # Remove everything, because there should never be duplicates.
        self.stack = [
            state for state in self.stack if state != self.target_states[stop]
        ]
        self.logger.log(__name__, "Stopping" + self.target_states[stop])

    def stop_intake(self) -> None:
        """
        Completely stops the intake by resetting the intake command stack.
        """
        self.stack = []
        self.logger.log(__name__, "Stopping all intake commands")
