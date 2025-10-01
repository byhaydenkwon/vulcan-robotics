"""
The pnuematic piston aligner at the front of the robot.
"""

from vex import *
from utils.display import Logger, NullLogger


class GoalAligner:
    def __init__(self, pneumatic: DigitalOut, logger: Logger | NullLogger) -> None:
        self.pneumatic = pneumatic
        self.logger = logger
        self.extended = False
        self.retract()

    def extend(self) -> None:
        """
        Extend the pneumatic goal aligner.
        """
        self.pneumatic.set(False)
        self.extended = True
        self.logger.log(__name__, "Goal aligner extended")

    def retract(self) -> None:
        """
        Retract the pneumatic goal aligner.
        """
        self.pneumatic.set(True)
        self.extended = False
        self.logger.log(__name__, "Goal aligner retracted")
