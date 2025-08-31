from vex import *


class Hopper:
    def __init__(self, motor: Motor, block_degrees: int, velocity_percent=100) -> None:
        self._motor = motor
        self.velocity = velocity_percent
        self.block_degrees = block_degrees
        # number of degrees required for one block to output
        # maybe improve by sensors later

    def intake(self):
        self._motor.spin(FORWARD)

    def output(self, blocks: int) -> None:
        self._motor.spin_for(
            FORWARD, self.block_degrees * blocks, DEGREES, self.velocity, PERCENT, True
        )

    def flush(self) -> None:
        self._motor.spin(REVERSE)

    def stop(self) -> None:
        self._motor.stop(HOLD)
