# region VEXcode Generated Robot Configuration
from vex import *
import urandom  # type: ignore

# Brain should be defined by default
brain = Brain()

# Robot configuration code

# Drivetrain motors
front_right = Motor(Ports.PORT1, GearSetting.RATIO_6_1, True)
middle_right = Motor(Ports.PORT2, GearSetting.RATIO_6_1, False)
back_right = Motor(Ports.PORT3, GearSetting.RATIO_6_1, False)
front_left = Motor(Ports.PORT4, GearSetting.RATIO_6_1, True)
middle_left = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
back_left = Motor(Ports.PORT6, GearSetting.RATIO_6_1, False)

# Auxillary motors
hopper_gate = Motor(Ports.PORT11)  # half motor
# NOTE I don't know exactly what our hopper gate design will be
# at this point, so most hopper code is best-guess
intake_bottom = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
intake_top = Motor(Ports.PORT13)  # half motor

# Sensors
inertial_sensor = Inertial(Ports.PORT7)
optical_sensor = Optical(Ports.PORT8)
gps_sensor = Gps(Ports.PORT9, 0, 0, DistanceUnits.MM, 180)
block_color_sensor = Optical(Ports.PORT10)

henry = DigitalOut(brain.three_wire_port.a)  # Tube intake (pneumatic)


controller_1 = Controller(PRIMARY)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = (
        brain.battery.voltage(MV)
        + brain.battery.current(CurrentUnits.AMP) * 100
        + brain.timer.system_high_res()
    )
    urandom.seed(int(random))


# Set random seed
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)


# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

# endregion VEXcode Generated Robot Configuration

# ------------------------------------------
#
# 	Project:
# 	Author:
# 	Created:
# 	Configuration:
#
# ------------------------------------------

# Begin project code

class AutoHopper:
    def __init__(self, motor: Motor):
        self._motor = motor
    
    def open(self):
        self._motor.spin_for(FORWARD, 180, DEGREES, wait=False)
    
    def close(self):
        self._motor.spin_for(REVERSE, 180, DEGREES, wait=False)

class Intake:
    def __init__(self, bottom_motor: Motor, top_motor: Motor, hopper: AutoHopper) -> None:
        self.bottom = bottom_motor
        self.top = top_motor
        self.hopper = hopper

    def start_intake(
        self, velocity: int, duration: int | None = None, auto_hopper=True
    ) -> None:
        """
        Starts the intake for the specified duration in milliseconds.
        Runs indefinitely if no duration is provided.
        Velocity must be provided as a percentage.

        If auto_hopper is True, this function also retracts the hopper gate.
        """
        self.bottom.set_velocity(velocity, PERCENT)
        if auto_hopper:
            self.hopper.open()
        if duration:
            timer = Timer()
            timer.event(self.stop_intake, duration)

    def stop_intake(self, auto_hopper=True) -> None:
        """
        Stops the intake.
        If auto_hopper is True, this function also restores the hopper gate.
        """
        self.bottom.set_velocity(0, PERCENT)
        if auto_hopper:
            self.hopper.close()


class AutonomousControl:
    def pre(self) -> None:
        gps_sensor.calibrate()
        while gps_sensor.is_calibrating():
            brain.screen.clear_screen()
            brain.screen.print("GPS sensor calibrating")
            wait(100, TimeUnits.MSEC)

        inertial_sensor.calibrate()
        while gps_sensor.is_calibrating():
            brain.screen.clear_screen()
            brain.screen.print("Inertial sensor calibrating")
            wait(100, TimeUnits.MSEC)

        optical_sensor.set_light(100)
        # TODO Have a way to recalibrate after a field adjustment or similar
        # Right now you can just restart the code
        # TODO have a set starting position for the GPS sensor

    def main(self) -> None:
        brain.screen.clear_screen()
        brain.screen.print("autonomous code not implemented")


class DriverControl:
    """
    Driver control class. Set the initial control mode during initalization (must be valid).
    Run start_control_loop() to start the driver control loop.
    """

    def __init__(self, control_mode: str, **kwargs) -> None:
        self.modes = {"split_arcade": self._split_arcade}
        self._control_mode = self.modes[control_mode]
        self._next_stop_control = False
        self._control_mode_kwargs = kwargs

    def start_control_loop(self) -> None:
        """
        Starts the driver control loop. Stops on control mode change or manual stop.
        """
        initial_control_mode = self._control_mode
        while not self._next_stop_control:
            if initial_control_mode != self._control_mode:
                self._next_stop_control = True
            self._control_mode(**self._control_mode_kwargs)

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
        self._control_mode = self.modes[control_mode]

    def get_control_mode(self) -> str:
        """
        Gets the currently running control mode as a string
        matching the internal map.
        """
        return {v: k for k, v in self.modes.items()}[self._control_mode]
        # reverse dict lookup of self.modes

    def _split_arcade(self) -> None:
        """
        Simple six-motor split arcade drive.
        """
        front_right.set_velocity(
            controller_1.axis3.position() + controller_1.axis1.position(), PERCENT
        )
        middle_right.set_velocity(
            controller_1.axis3.position() + controller_1.axis1.position(), PERCENT
        )
        back_right.set_velocity(
            controller_1.axis3.position() + controller_1.axis1.position(), PERCENT
        )

        front_left.set_velocity(
            controller_1.axis3.position() - controller_1.axis1.position(), PERCENT
        )
        middle_left.set_velocity(
            controller_1.axis3.position() - controller_1.axis1.position(), PERCENT
        )
        back_left.set_velocity(
            controller_1.axis3.position() - controller_1.axis1.position(), PERCENT
        )


driver = DriverControl("split_arcade")
auto = AutonomousControl()

comp = Competition(driver.start_control_loop, auto.main)
auto.pre()
