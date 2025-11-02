"""
The pnuematic piston aligner at the front of the robot.
"""

from vex import *

from utils.display import Logger, NullLogger


class PneumaticToggle:
    def __init__(
        self,
        pneumatic: DigitalOut,
        internal_extended_bool: bool,
        default_extended_status: bool,
        logger: Logger | NullLogger,
        name="Pneumatic component",
    ) -> None:
        """
        Base class for togglable pneumatic components.

        pneumatic: The DigitalOut pneumatic port.
        internal_extended_out_bool: The status of the extended pneumatic component,
            as called to DigitalOut.set(status).
        default_extended_status: The default status of the pneumatic component, where
            True is extended and False is retracted.
        logger: The Logger used for this component.
        name: The name used in logs for this component. By default, "pneumatic component".
        """
        self.logger = logger
        self.name = name

        self._EXTENDED_BOOL = internal_extended_bool
        self.pneumatic = pneumatic

        self.extended = default_extended_status

        if default_extended_status:
            self.extend()
        else:
            self.retract()

    def extend(self) -> None:
        """
        Extend the pneumatic component.
        """
        self.pneumatic.set(False)
        self.extended = True
        self.logger.log(__name__, self.name + " extended")

    def retract(self) -> None:
        """
        Retract the pneumatic component.
        """
        self.pneumatic.set(True)
        self.extended = False
        self.logger.log(__name__, self.name + " retracted")

    def toggle(self) -> None:
        """
        Toggle the pneumatic component.
        """
        if self.extended:
            self.retract()
        else:
            self.extend()


class GoalAligner(PneumaticToggle):
    def __init__(
        self,
        pneumatic: DigitalOut,
        internal_extended_bool: bool,
        default_extended_status: bool,
        logger: Logger | NullLogger,
    ) -> None:
        super().__init__(
            pneumatic,
            internal_extended_bool,
            default_extended_status,
            logger,
            "Goal aligner",
        )


class MatchLoader(PneumaticToggle):
    def __init__(
        self,
        pneumatic: DigitalOut,
        internal_extended_bool: bool,
        default_extended_status: bool,
        logger: Logger | NullLogger,
    ) -> None:
        super().__init__(
            pneumatic,
            internal_extended_bool,
            default_extended_status,
            logger,
            "Match loader",
        )
