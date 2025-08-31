"""
Contains the DriverControl class with related drive and control functions.
"""

from vex import *

import config

from mechanisms.hopper import Hopper
from mechanisms.intake import Intake


class DriverControl:
    """
    Driver control class. Set the initial control mode during initalization (must be valid).
    Run start_control_loop() to start the driver control loop.
    """

    def __init__(
        self,
        drive_mode: str,
        mechanism_mode: str,
        controller: Controller,
        intake: Intake,
        hopper: Hopper,
        **kwargs,
    ) -> None:
        self.drive_modes = {"split_arcade": self._split_arcade}
        self.mechanism_modes = {"standard": self._standard_mechanisms}

        self._drive_mode = self.drive_modes[drive_mode]
        self._drive_mode_kwargs = kwargs
        self._next_stop_control = False

        self._mechanism_mode = self.mechanism_modes[mechanism_mode]

        self.controller = controller
        self.intake = intake
        self.hopper = hopper

    def start_control_loop(self) -> None:
        """
        Starts the driver control loop. Stops on control mode change or manual stop.
        """
        initial_control_mode = self._drive_mode
        while not self._next_stop_control:
            if initial_control_mode != self._drive_mode:
                self._next_stop_control = True
            self._drive_mode(**self._drive_mode_kwargs)

    def stop_control_loop(self) -> None:
        """
        Stops the driver control loop.
        """
        self._next_stop_control = True

    def set_control_mode(self, control_mode: str) -> None:
        """
        Sets the driver control mode. Must be a valid value
        as defined in the class constructor (modes).

        This function stops the currently running control loop.
        Run start_control_loop() to restart it.
        """
        self._drive_mode = self.drive_modes[control_mode]

    def get_control_mode(self) -> str:
        """
        Gets the currently running control mode as a string
        matching the internal map.
        """
        return {v: k for k, v in self.drive_modes.items()}[self._drive_mode]
        # reverse dict lookup of self.modes

    def _split_arcade(self) -> None:
        """
        Simple six-motor split arcade drive.
        """
        for motor in [config.front_right, config.middle_right, config.back_right]:
            motor.set_velocity(
                max(
                    min(
                        config.controller_1.axis3.position()
                        - config.controller_1.axis1.position(),
                        100,
                    ),
                    -100,
                ),
                PERCENT,
            )
            motor.spin(FORWARD)

        for motor in [config.front_left, config.middle_left, config.back_left]:
            motor.set_velocity(
                max(
                    min(
                        config.controller_1.axis3.position()
                        + config.controller_1.axis1.position(),
                        100,
                    ),
                    -100,
                ),
                PERCENT,
            )
            motor.spin(FORWARD)

        if "DRIVE" in config.DEBUG_MODES:
            config.brain.screen.print_at(
                "Right Motors Target Velocity: "
                + str(
                    max(
                        min(
                            config.controller_1.axis3.position()
                            + config.controller_1.axis1.position(),
                            100,
                        ),
                        -100,
                    )
                ),
                y=50,
                x=0,
            )
            config.brain.screen.print_at(
                "Left Motors Target Velocity: "
                + str(
                    max(
                        min(
                            config.controller_1.axis3.position()
                            - config.controller_1.axis1.position(),
                            100,
                        ),
                        -100,
                    )
                ),
                y=80,
                x=0,
            )

            wait(10)
            config.brain.screen.clear_screen()

            # brain.screen.print("Mid Right Velocity: " + str(middle_right.velocity(PERCENT)))
            # brain.screen.new_line()
            # brain.screen.print("Back Right Velocity: " + str(back_right.velocity(PERCENT)))
            # brain.screen.new_line()

            # brain.screen.print("Front Left Velocity: " + str(front_left.velocity(PERCENT)))
            # brain.screen.new_line()
            # brain.screen.print("Mid Left Velocity: " + str(middle_left.velocity(PERCENT)))
            # brain.screen.new_line()
            # brain.screen.print("Back Left Velocity: " + str(back_left.velocity(PERCENT)))
            # brain.screen.new_line()

    # TODO Make turning and driving speed configurable in new driving function

    def _standard_mechanisms(self) -> None:
        self.controller.buttonR1.pressed(lambda: self.intake.start_intake(100))
        self.controller.buttonR1.released(lambda: self.intake.stop_intake())
