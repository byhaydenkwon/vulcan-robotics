from vex import *
import urandom  # type: ignore

# Config

brain = Brain()

# Drivetrain motors
front_right = Motor(Ports.PORT1, GearSetting.RATIO_6_1, True)
middle_right = Motor(Ports.PORT2, GearSetting.RATIO_6_1, True)
back_right = Motor(Ports.PORT3, GearSetting.RATIO_6_1, False)
front_left = Motor(Ports.PORT4, GearSetting.RATIO_6_1, True)
middle_left = Motor(Ports.PORT5, GearSetting.RATIO_6_1, True)
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

# Currently only DRIVE is implemented.
# Eventually should add INTAKE, HOPPER, etc.
DEBUG_MODES = ["DRIVE"]


def main() -> None:
    setup()

    hopper = AutoHopper(hopper_gate)
    intake = Intake(intake_bottom, intake_top, hopper, controller_1)

    driver = DriverControl("split_arcade", "standard", controller_1, intake, hopper)
    auto = AutonomousControl()

    comp = Competition(driver.start_control_loop, auto.main)
    auto.pre()


def initializeRandomSeed() -> None:
    wait(100, MSEC)
    random = (
        brain.battery.voltage(MV)
        + brain.battery.current(CurrentUnits.AMP) * 100
        + brain.timer.system_high_res()
    )
    urandom.seed(int(random))


def setup() -> None:
    """
    A setup function containing mostly VEXCode generated code.
    """

    # wait for rotation sensor to fully initialize
    wait(30, MSEC)

    # Set random seed
    initializeRandomSeed()

    # add a small delay to make sure we don't print in the middle of the REPL header
    wait(200, MSEC)
    # clear the console to make sure we don't have the REPL in the console
    print("\033[2J")


class AutoHopper:
    def __init__(self, motor: Motor):
        self._motor = motor

    def open(self):
        self._motor.spin_for(FORWARD, 180, DEGREES, wait=False)

    def close(self):
        self._motor.spin_for(REVERSE, 180, DEGREES, wait=False)


class Intake:
    def __init__(
        self,
        bottom_motor: Motor,
        top_motor: Motor,
        hopper: AutoHopper,
        controller: Controller,
    ) -> None:
        self.bottom = bottom_motor
        self.top = top_motor
        self.hopper = hopper
        self.controller = controller

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
        # gps_sensor.calibrate()
        # while gps_sensor.is_calibrating():
        #     brain.screen.clear_screen()
        #     brain.screen.print("GPS sensor calibrating")
        #     wait(100, TimeUnits.MSEC)

        # inertial_sensor.calibrate()
        # while gps_sensor.is_calibrating():
        #     brain.screen.clear_screen()
        #     brain.screen.print("Inertial sensor calibrating")
        #     wait(100, TimeUnits.MSEC)

        # optical_sensor.set_light(100)

        pass
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

    def __init__(
        self,
        drive_mode: str,
        mechanism_mode: str,
        controller: Controller,
        intake: Intake,
        hopper: AutoHopper,
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
        for motor in [front_right, middle_right, back_right]:
            motor.set_velocity(
                max(min(controller_1.axis3.position() + controller_1.axis1.position(), 100), -100),
                PERCENT,
            )

        for motor in [front_left, middle_left, back_left]:
            motor.set_velocity(
                max(min(controller_1.axis3.position() - controller_1.axis1.position(), 100), -100),
                PERCENT,
            )

        if "DRIVE" in DEBUG_MODES:
            brain.screen.print_at(
                "Right Motors Target Velocity: "
                + str(
                    max(
                        controller_1.axis3.position() + controller_1.axis1.position(),
                        100,
                    )
                ),
                y=50,
                x=0,
            )
            brain.screen.print_at(
                "Left Motors Target Velocity: "
                + str(
                    max(
                        controller_1.axis3.position() - controller_1.axis1.position(),
                        100,
                    )
                ),
                y=60,
                x=0,
            )

            wait(10)
            brain.screen.clear_screen()

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

    def _standard_mechanisms(self) -> None:
        self.controller.buttonR1.pressed(lambda: self.intake.start_intake(100))
        self.controller.buttonR1.released(lambda: self.intake.stop_intake())


if __name__ == "__main__":
    main()
