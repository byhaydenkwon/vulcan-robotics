"""
Contains the AutonomousControl class for autonomous code.
"""

from vex import *

import mechanisms.odometry as odometry
from utils.display import Logger, NullLogger
from utils.enums import IntakeTargets
from mechanisms.intake import Intake
from mechanisms.pneumatics import GoalAligner, MatchLoader


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
        intake: Intake,
        inertial: Inertial,
        optical: Optical,
        gps: Gps,
        block_color: Optical,
        loader: MatchLoader,
        aligner: GoalAligner,
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

        self.intake = intake
        self.inertial = inertial
        self.optical = optical
        self.gps = gps
        self.block_color = block_color
        self.loader = loader
        self.aligner = aligner

        self.tracking = tracking

        self.drivetrain_velocity = drivetrain_velocity
        self.turn_velocity = turn_velocity

        self.logger = logger

        self._stop = False

    def match_auton(self, goal_turn_direction: TurnType.TurnType) -> None:
        """
        RIGHT for positions 2 and 3; LEFT for positions 1 and 4.
        """
        try:
            self.pivot_turn(5, goal_turn_direction, 5)
            self.intake.start_intake()
            self.drive(FORWARD, 40.0, 35)
            wait(1, SECONDS)
            self.drive(REVERSE, 35.0, 25)
            self.intake.stop_intake()
            self.pivot_turn(75, goal_turn_direction, 20)
            self.drive(FORWARD, 28.5, 25)
            self.pivot_turn(85, LEFT if goal_turn_direction is RIGHT else RIGHT, 20)
            self.aligner.extend()
            self.drive(FORWARD, 30.0, 50)
            self.intake.output(IntakeTargets.HIGH)
        except AutonomousExit as e:
            self.logger.log(__name__, e.args[0])

    def skills_auton(self) -> None:
        self.intake.output(IntakeTargets.LOW)
        self.drive(FORWARD, 24, 60)

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

        if turn_target <= 6:
            lower_turn_difference = turn_target - turn_target * 0.25
            upper_turn_difference = turn_target + turn_target * 0.25
        else:
            lower_turn_difference = turn_target - 2.5
            upper_turn_difference = turn_target + 2.5
        # Allow for 2.5 degrees of error in each direction, or 5 degrees total.
        # 25% if the target itself is less than 6 degrees; maximum 3 deg total range in this case.
        # Try adjusting this value if it doesn't like turning lower values.

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
        self.intake.stop_intake()
        self.logger.log(__name__, "Autonomous code stopped")

    @staticmethod
    def i_do_nothing_replace_me(*args, **kwargs) -> None:
        """
        Do nothing.
        Dummy autonomous code function.
        """
        pass
