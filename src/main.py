# region VEXcode Generated Robot Configuration
from vex import *
import urandom  # type: ignore

# Brain should be defined by default
brain = Brain()

# Robot configuration code
front_right = Motor(Ports.PORT1, GearSetting.RATIO_6_1, False)
middle_right = Motor(Ports.PORT2, GearSetting.RATIO_6_1, False)
back_right = Motor(Ports.PORT3, GearSetting.RATIO_6_1, False)
front_left = Motor(Ports.PORT4, GearSetting.RATIO_6_1, False)
middle_left = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
back_left = Motor(Ports.PORT6, GearSetting.RATIO_6_1, False)
inertial_sensor = Inertial(Ports.PORT7)
optical_sensor = Optical(Ports.PORT8)
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


def pre_autonomous() -> None:
    # actions to do when the program starts
    brain.screen.clear_screen()
    brain.screen.print("pre auton code")
    wait(1, SECONDS)


def autonomous() -> None:
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here


def user_control() -> None:
    brain.screen.clear_screen()
    while True:
        # maybe implement cheesy drive TODO?
        front_right.set_velocity(
            controller_1.axis3.position() + controller_1.axis1.position()
        )
        middle_right.set_velocity(
            controller_1.axis3.position() + controller_1.axis1.position()
        )
        back_right.set_velocity(
            controller_1.axis3.position() + controller_1.axis1.position()
        )

        front_left.set_velocity(
            controller_1.axis3.position() - controller_1.axis1.position()
        )
        middle_left.set_velocity(
            controller_1.axis3.position() - controller_1.axis1.position()
        )
        back_left.set_velocity(
            controller_1.axis3.position() - controller_1.axis1.position()
        )


# create competition instance
comp = Competition(user_control, autonomous)
pre_autonomous()
