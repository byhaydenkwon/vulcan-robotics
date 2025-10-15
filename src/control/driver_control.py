"""
Contains the DriverControl class with related drive and control functions.
"""

from vex import *

from utils.display import Logger, NullLogger

from mechanisms.hopper import Hopper
from mechanisms.intake import Intake
from mechanisms.aligner import GoalAligner


class DriverControl:
    """
    Driver control class. Set the initial control mode during initalization (must be valid).
    Run start_control_loop() to start the driver control loop.
    """

    def __init__(
        self,
        drive_mode: str,
        mechanism_mode: str,
        front_right: Motor,
        middle_right: Motor,
        back_right: Motor,
        front_left: Motor,
        middle_left: Motor,
        back_left: Motor,
        controller: Controller,
        intake: Intake,
        hopper: Hopper,
        aligner: GoalAligner,
        logger: Logger | NullLogger = NullLogger(),
        **kwargs,
    ) -> None:
        self.drive_modes = {"split_arcade": self._split_arcade}
        self.mechanism_modes = {"standard": self._standard_mechanisms}

        self.front_right = front_right
        self.middle_right = middle_right
        self.back_right = back_right
        self.front_left = front_left
        self.middle_left = middle_left
        self.back_left = back_left

        self._drive_mode = self.drive_modes[drive_mode]
        self._drive_mode_kwargs = kwargs
        self._next_stop_control = False

        self._mechanism_mode = self.mechanism_modes[mechanism_mode]

        self.controller = controller
        self.intake = intake
        self.hopper = hopper
        self.aligner = aligner

        self.logger = logger

    def start_control_loop(self) -> None:
        """
        Starts the driver control loop. Stops on control mode change or manual stop.
        """

        self._mechanism_mode()
        self.logger.log(__name__, "Starting driver control loop")

        initial_drive_mode = self._drive_mode

        self.logger.log(__name__, "Initial drive mode: " + str(initial_drive_mode))

        while not self._next_stop_control:
            if initial_drive_mode != self._drive_mode:
                self.logger.log(
                    __name__, "Drive mode change detected, stopping control loop"
                )
                self._next_stop_control = True
            self._drive_mode(**self._drive_mode_kwargs)

            sleep(2)

    def stop_control_loop(self) -> None:
        """
        Stops the driver control loop.
        """
        self._next_stop_control = True

        self.logger.log(__name__, "Stopping driver control loop")

    def set_control_mode(self, control_mode: str) -> None:
        """
        Sets the driver control mode. Must be a valid value
        as defined in the class constructor (modes).

        This function stops the currently running control loop.
        Run start_control_loop() to restart it.
        """
        self._drive_mode = self.drive_modes[control_mode]

        self.logger.log(__name__, "Drive mode set to " + control_mode)

    def get_control_mode(self) -> str:
        """
        Gets the currently running control mode as a string
        matching the internal map.
        """
        return {v: k for k, v in self.drive_modes.items()}[self._drive_mode]
        # reverse dict lookup of self.modes

    def _split_arcade(self, velocity: int, turn_velocity: float) -> None:
        """
        Simple six-motor split arcade drive.
        Provide velocity and turn velocity as percentages.
        """

        y_input = self.controller.axis3.position() * velocity / 100
        x_input = self.controller.axis1.position() * turn_velocity / 100

        for motor in [self.front_right, self.middle_right, self.back_right]:
            motor.set_velocity(y_input - x_input, PERCENT)
            motor.spin(FORWARD)

        for motor in [self.front_left, self.middle_left, self.back_left]:
            motor.set_velocity(y_input + x_input, PERCENT)
            motor.spin(FORWARD)

    def _standard_mechanisms(self) -> None:
        self.controller.buttonR1.pressed(lambda: self.intake.start_intake(100))
        self.controller.buttonR1.released(lambda: self.intake.stop_intake())

        self.controller.buttonR2.pressed(lambda: self.intake.output_bottom_goal(100))
        self.controller.buttonR2.released(self.intake.stop_intake)

        self.controller.buttonL1.pressed(lambda: self.intake.output_top_goal(100))
        self.controller.buttonL1.released(self.intake.stop_intake)

        self.controller.buttonL2.pressed(lambda: self.intake.output_middle_goal(100))
        self.controller.buttonL2.released(self.intake.stop_intake)

        self.controller.buttonA.pressed(lambda: self.aligner.toggle())

        # y: future wing control
        # left: future tube intake
        # right: alignment mech
