"""
Contains the AutonomousControl class for autonomous and pre-autonomous code.
"""

from vex import *

from display import Logger, NullLogger


class AutonomousControl:
    """
    Main autonomous control class.
    Contains entry functions for pre-autonomous and autonomous code.
    """

    def __init__(
        self,
        logger: Logger | NullLogger = NullLogger(),
    ):
        self.logger = logger

    @staticmethod
    def i_do_nothing_replace_me(*args, **kwargs) -> None:
        """
        Do nothing.
        Dummy autonomous code function.
        """
        pass
