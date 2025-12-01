"""
Contains the AutonomousControl class for autonomous code.
"""

from vex import *

from utils.display import Logger, NullLogger
from utils.enums import ScoringTargets

from mechanisms.drivetrain import Drivetrain
from mechanisms.scoring import Scoring
from mechanisms.pneumatics import PneumaticToggle


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
        drivetrain: Drivetrain,
        scoring: Scoring,
        inertial: Inertial,
        loader: PneumaticToggle,
        aligner: PneumaticToggle,
        logger: Logger | NullLogger = NullLogger(),
    ):
        self.drivetrain = drivetrain
        self.scoring = scoring
        self.loader = loader
        self.aligner = aligner

        self.inertial = inertial

        self.logger = logger

        self._stop = False

    def match_auton(self, goal_turn_direction: TurnType.TurnType) -> None:
        """
        RIGHT for positions 2 and 3; LEFT for positions 1 and 4.
        """
        try:
            opposite_direction = LEFT if goal_turn_direction is RIGHT else RIGHT
            self.pivot_turn(1, goal_turn_direction, 5)
            self.scoring.start_intake()
            self.drive(FORWARD, 40.0, 35)
            wait(1.5, SECONDS)
            self.drive(REVERSE, 8.0, 25)
            self.scoring.stop_command(ScoringTargets.INTAKE)
            self.pivot_turn(123, goal_turn_direction, 20)
            self.drive(REVERSE, 2.5, 50)
            self.scoring.output(ScoringTargets.MIDDLE)

        except AutonomousExit as e:
            self.logger.log(__name__, e.args[0])

    def skills_auton(self) -> None:
        self.scoring.output(ScoringTargets.LOW)
        self.drive(FORWARD, 24, 60)

    def drive(
        self,
        direction: DirectionType.DirectionType,
        distance: float,
        velocity: float,
    ) -> None:
        """
        Autonomously drive a specified distance at a specified velocity.
        """
        if self._stop:
            raise AutonomousExit("Autonomous exit during drive")

        self.drivetrain.reset_tracking()
        self.drivetrain.spin_motors(direction, velocity)

        while self.drivetrain.get_distance_traveled() < distance:
            pass

        self.drivetrain.stop_motors()

    def pivot_turn(
        self, degrees: float, direction: TurnType.TurnType, velocity: float
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

        if direction == TurnType.LEFT:
            self.drivetrain.spin_right_motors(FORWARD, velocity)
            self.drivetrain.spin_left_motors(REVERSE, velocity)
        else:
            self.drivetrain.spin_left_motors(FORWARD, velocity)
            self.drivetrain.spin_right_motors(REVERSE, velocity)

        while (
            self.inertial.heading() < lower_turn_difference
            or self.inertial.heading() > upper_turn_difference
        ):  # outside of acceptable range
            pass

        self.drivetrain.stop_motors()

    def exit_autonomous(self) -> None:
        """
        Stop all mechanisms and exit all autonomous routines.
        """
        # raise AutonomousExit in drivetrain functions if routine not finished
        self._stop = True
        self.drivetrain.stop_motors()
        self.scoring.stop_intake()
        self.logger.log(__name__, "Autonomous code stopped")

    @staticmethod
    def i_do_nothing_replace_me(*args, **kwargs) -> None:
        """
        Do nothing.
        Dummy autonomous code function.
        """
        pass
