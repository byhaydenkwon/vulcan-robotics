"""
Contains the Hopper class.
"""

from vex import *

from utils.display import Logger, NullLogger


class Hopper:
    def __init__(
        self,
        motor: Motor,
        block_degrees: int,
        velocity_percent=100,
        logger: Logger | NullLogger = NullLogger(),
    ) -> None:
        self._motor = motor
        self.velocity = velocity_percent
        self.block_degrees = block_degrees
        # number of degrees required for one block to output
        # maybe improve by sensors later
        self.logger = logger

    def intake(self):
        self._motor.spin(FORWARD, velocity=self.velocity)
        self.logger.log(__name__, "Starting hopper intake")

    def output(self, blocks: int) -> None:
        self._motor.spin_for(
            FORWARD, self.block_degrees * blocks, DEGREES, self.velocity, PERCENT, True
        )
        self.logger.log(__name__, "Hopper releasing " + str(blocks) + "blocks")

    def flush(self) -> None:
        self._motor.spin(REVERSE, velocity=self.velocity)
        self.logger.log(__name__, "Hopper flushing")

    def stop(self) -> None:
        self._motor.stop()
        self.logger.log(__name__, "Hopper stopping")
