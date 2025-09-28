"""
Contains the AutonomousControl class for autonomous code.
"""

from vex import *

import mechanisms.odometry as odometry
from utils.display import Logger, NullLogger
from mechanisms.hopper import Hopper
from mechanisms.intake import Intake


class AutonomousExit(Exception):
    """
    Exception raised to stop autonomous code when the driver control period starts.
    """

    pass


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
        tracking: odometry.DrivetrainOdometry | odometry.LinearOdometry,
        drivetrain_velocity: int,
        turn_velocity: int,
        logger: Logger | NullLogger = NullLogger(),
    ):
        self.front_right = front_right
        self.middle_right = middle_right
        self.back_right = back_right
        self.front_left = front_left
        self.middle_left = middle_left
        self.back_left = back_left

        # The order of this list determines the motor starting and stopping order
        self.drivetrain = [
            back_right,
            back_left,
            middle_right,
            middle_left,
            front_right,
            front_left,
        ]

        self.right_drivetrain = [back_right, middle_right, front_right]
        self.left_drivetrain = [back_left, middle_left, front_left]

        self.hopper = hopper
        self.intake = intake
        self.inertial = inertial
        self.optical = optical
        self.gps = gps
        self.block_color = block_color
        self.tube_pneumatic = tube_pneumatic

        self.tracking = tracking

        self.drivetrain_velocity = drivetrain_velocity
        self.turn_velocity = turn_velocity

        self.logger = logger

        self._stop = False

    # TODO: Combine these functions into one that has direction parameters
    def position_1_match_auton(self) -> None:
        pass

    def position_2_match_auton(self) -> None:
        try:
            self.drive(FORWARD, 200.0, 1)
        except AutonomousExit as e:
            self.logger.log(__name__, e.args[0])

    def position_3_match_auton(self) -> None:
        try:
            self.intake.start_intake(100)
            self.pivot_turn(10, RIGHT, 10)
            self.drive(FORWARD, 40.0, 50)
            if not self._stop:
                wait(2, SECONDS)
            self.drive(REVERSE, 20.0, 50)
            self.intake.stop_intake()
            self.pivot_turn(80, RIGHT, 20)
            self.drive(FORWARD, 30.0, 50)
            self.pivot_turn(90, LEFT, 20)
            self.intake.start_intake(100)
            self.drive(FORWARD, 10.0, 30)
            self.intake.stop_intake()
        except AutonomousExit as e:
            self.logger.log(__name__, e.args[0])

    def position_4_match_auton(self) -> None:
        pass

    def drive(
        self,
        direction: DirectionType.DirectionType,
        distance: float,
        velocity: int | None,
    ) -> None:
        """
        Autonomously drive a specified distance at a specified velocity.
        """
        if self._stop:
            raise AutonomousExit("Autonomous exit during drive")

        self.tracking.reset_tracking()
        Thread(self.tracking.start_tracking)

        for motor in self.drivetrain:
            motor.set_velocity(
                velocity if velocity is not None else self.drivetrain_velocity, PERCENT
            )
            motor.spin(direction, velocity, PERCENT)

        while self.tracking.get_distance_traveled() < distance:
            pass

        for motor in self.drivetrain:
            motor.stop()

    def pivot_turn(
        self, degrees: float, direction: TurnType.TurnType, velocity: int | None
    ) -> None:
        """
        Autonomously turn in place using all wheels. Loses accuracy at higher speeds.
        """
        # NOTE Relies only on the inertial sensor for now.

        if self._stop:
            raise AutonomousExit("Autonomous exit during pivot turn")

        if direction == TurnType.UNDEFINED:
            return

        self.inertial.reset_heading()

        turn_target = degrees if direction == TurnType.RIGHT else -degrees + 360
        lower_turn_difference = turn_target - turn_target * 0.025
        upper_turn_difference = turn_target + turn_target * 0.025
        # Allow for x% of error.
        # This does mean that if it's not detected the first time, it will
        # make a 360 degree rotation before trying to stop again.

        forward_motors = (
            self.right_drivetrain
            if direction == TurnType.LEFT
            else self.left_drivetrain
        )

        for motor in self.drivetrain:
            motor.spin(
                FORWARD if motor in forward_motors else REVERSE, velocity, PERCENT
            )

        while (
            self.inertial.heading() < lower_turn_difference
            or self.inertial.heading() > upper_turn_difference
        ):  # outside of acceptable range
            pass

        for motor in self.drivetrain:
            motor.stop()

    def exit_autonomous(self) -> None:
        """
        Stop all mechanisms and exit all autonomous routines.
        """
        # raise AutonomousExit in drivetrain functions if routine not finished
        self._stop = True
        for motor in self.drivetrain:
            motor.stop()
        self.hopper.stop()
        self.intake.stop_intake(auto_hopper=False)
        self.tracking.stop_tracking()
        self.logger.log(__name__, "Autonomous code stopped")

    @staticmethod
    def i_do_nothing_replace_me(*args, **kwargs) -> None:
        """
        Do nothing.
        Dummy autonomous code function.
        """
        pass
