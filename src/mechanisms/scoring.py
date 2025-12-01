"""
Contains the Intake class.
"""

from vex import *

from utils.enums import (
    ScoringStates,
    ScoringStateValue,
    ScoringTargets,
    ScoringTargetValue,
)
from utils.display import Logger, NullLogger


class Scoring:
    """
    A stack-based scoring control class.
    """

    def __init__(
        self,
        top_motor: Motor,
        middle_motor: Motor,
        intake_motor: Motor,
        hopper_motor: Motor,
        logger: Logger | NullLogger = NullLogger(),
    ) -> None:
        self.top = top_motor
        self.middle = middle_motor
        self.intake = intake_motor
        self.hopper = hopper_motor

        self.logger = logger

        self.target_states: dict[ScoringTargetValue, ScoringStateValue] = {
            ScoringTargets.INTAKE: ScoringStates.INTAKING,
            ScoringTargets.LOW: ScoringStates.SCORING_LOW,
            ScoringTargets.MIDDLE: ScoringStates.SCORING_MIDDLE,
            ScoringTargets.HIGH: ScoringStates.SCORING_HIGH,
        }

        # Okay, technically not a stack. Last in is not always first out.
        # But close enough.
        self.stack: list[ScoringStateValue] = []

        self._next_stop_control = False

    def start_control_loop(self) -> None:
        """
        Starts the scoring stack control loop.
        """
        while not self._next_stop_control:
            if not self.stack:
                active = ScoringStates.OFF
            else:
                try:
                    active = self.stack[-1]
                except IndexError:
                    pass  # this is REQUIRED or the robot will randomly break

            if active == ScoringStates.OFF:
                self.top.stop()
                self.middle.stop()
                self.intake.stop()
                self.hopper.stop()
            elif active == ScoringStates.INTAKING:
                self.top.stop()
                self.middle.spin(FORWARD, 100, PERCENT)
                self.intake.spin(FORWARD, 100, PERCENT)
                self.hopper.spin(FORWARD, 100, PERCENT)
            elif active == ScoringStates.SCORING_LOW:
                self.top.stop()
                self.middle.spin(REVERSE, 100, PERCENT)
                self.intake.spin(REVERSE, 100, PERCENT)
                self.hopper.spin(REVERSE, 100, PERCENT)
            elif active == ScoringStates.SCORING_MIDDLE:
                self.top.spin(REVERSE, 100, PERCENT)
                self.middle.spin(FORWARD, 100, PERCENT)
                self.intake.stop()
                self.hopper.spin(REVERSE, 100, PERCENT)
            elif active == ScoringStates.SCORING_HIGH:
                self.top.spin(FORWARD, 100, PERCENT)
                self.middle.spin(FORWARD, 100, PERCENT)
                self.intake.stop()
                self.hopper.spin(REVERSE, 100, PERCENT)
            if len(self.stack) > len(self.target_states):
                self.stack = self.stack[4:]
                # this prevents issues when the buttons are spammed extremely quickly

            wait(15, MSEC)

    def stop_control_loop(self) -> None:
        """
        Stops the scoring control loop.
        """
        self._next_stop_control = True

    def start_intake(self, duration: int | None = None) -> None:
        """
        Starts the intake for the specified duration in milliseconds.
        Runs indefinitely if no duration is provided.
        """

        if ScoringStates.INTAKING not in self.stack:
            self.stack.append(ScoringStates.INTAKING)

        if duration:
            timer = Timer()
            timer.event(lambda: self.stop_command(ScoringTargets.INTAKE), duration)

        self.logger.log(
            __name__,
            "Starting scoring + "
            + ("for " + str(duration) + "ms" if duration else "indefinitely"),
        )

    def output(self, target: ScoringTargetValue, duration: int | None = None):
        """
        Outputs blocks at the specified level for a duration in milliseconds.
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

    def stop_command(self, stop: ScoringTargetValue) -> None:
        """
        Removes all ScoringStates of the passed ScoringTarget from the command stack.
        """
        # Remove everything, because there should never be duplicates.
        self.stack = [
            state for state in self.stack if state != self.target_states[stop]
        ]
        self.logger.log(__name__, "Stopping" + self.target_states[stop])

    def stop_intake(self) -> None:
        """
        Completely stops scoring by resetting the command stack.
        """
        self.stack = []
        self.logger.log(__name__, "Stopping all scoring commands")
