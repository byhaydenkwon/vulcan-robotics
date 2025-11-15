"""
Contains the DriverControl class with related drive and control functions.
"""

from vex import *

from utils.enums import ScoringTargets
from utils.display import Logger, NullLogger

from mechanisms.drivetrain import Drivetrain
from mechanisms.scoring import Scoring
from mechanisms.pneumatics import PneumaticToggle


class DriverControl:
    """
    Driver control class. Set the initial control mode during initalization (must be valid).
    Run start_control_loop() to start the driver control loop.
    """

    def __init__(
        self,
        drive_mode: str,
        mechanism_mode: str,
        drivetrain: Drivetrain,
        controller: Controller,
        scoring: Scoring,
        aligner: PneumaticToggle,
        loader: PneumaticToggle,
        logger: Logger | NullLogger = NullLogger(),
        **kwargs,
    ) -> None:
        self.drive_modes = {"split_arcade": self._split_arcade}
        self.mechanism_modes = {
            "standard": [self._standard_mechanisms, self._pre_register_mechanisms]
        }

        self._drive_mode = self.drive_modes[drive_mode]
        self._drive_mode_kwargs = kwargs
        self._next_stop_control = False

        self._mechanism_mode = self.mechanism_modes[mechanism_mode]

        self.controller = controller
        self.drivetrain = drivetrain
        self.scoring = scoring
        self.aligner = aligner
        self.loader = loader

        self.logger = logger

    def start_control_loop(self) -> None:
        """
        Starts the driver control loop. Stops on control mode change or manual stop.
        """
        self.logger.log(__name__, "Starting driver control loop")

        initial_drive_mode = self._drive_mode

        self.logger.log(__name__, "Initial drive mode: " + str(initial_drive_mode))

        self._mechanism_mode[1]()

        while not self._next_stop_control:
            if initial_drive_mode != self._drive_mode:
                self.logger.log(
                    __name__, "Drive mode change detected, stopping control loop"
                )
                self._next_stop_control = True
            self._drive_mode(**self._drive_mode_kwargs)
            self._mechanism_mode[0]()

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

        self.drivetrain.spin_right_motors(FORWARD, y_input - x_input)
        self.drivetrain.spin_left_motors(FORWARD, y_input + x_input)

    def _standard_mechanisms(self) -> None:
        # callbacks not used to enable holding down buttons during
        # autonomous period and immediately having the functions call
        # when the driver control period starts
        if self.controller.buttonR1.pressing():
            self.scoring.start_intake()
        else:
            self.scoring.stop_command(ScoringTargets.INTAKE)

        if self.controller.buttonR2.pressing():
            self.scoring.output(ScoringTargets.LOW)
        else:
            self.scoring.stop_command(ScoringTargets.LOW)

        if self.controller.buttonL1.pressing():
            self.scoring.output(ScoringTargets.HIGH)
        else:
            self.scoring.stop_command(ScoringTargets.HIGH)

        if self.controller.buttonL2.pressing():
            self.scoring.output(ScoringTargets.MIDDLE)
        else:
            self.scoring.stop_command(ScoringTargets.MIDDLE)

        if self.controller.buttonDown.pressing():
            self.scoring.stop_intake()

        # y: future wing control
        # left: future tube intake

    def _pre_register_mechanisms(self) -> None:
        def smart_toggle_pneumatics() -> None:
            if self.aligner.extended:
                self.loader.extend()
                Timer().event(self.aligner.retract, 100)
            else:
                self.aligner.extend()
                Timer().event(self.loader.retract, 100)

        self.controller.buttonA.pressed(smart_toggle_pneumatics)
