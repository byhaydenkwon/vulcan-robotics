"""
Contains builtin VEX motors and sensors as well as constants.
"""

from vex import *

brain = Brain()

# True = reversed, False = normal

# Drivetrain motors
front_right = Motor(Ports.PORT13, GearSetting.RATIO_6_1, False)
middle_right = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
back_right = Motor(Ports.PORT20, GearSetting.RATIO_6_1, False)
front_left = Motor(Ports.PORT18, GearSetting.RATIO_6_1, True)
middle_left = Motor(Ports.PORT19, GearSetting.RATIO_6_1, True)
back_left = Motor(Ports.PORT11, GearSetting.RATIO_6_1, True)

drivetrain_motors = [
    front_right,
    middle_right,
    back_right,
    front_left,
    middle_left,
    back_left,
]

# Auxillary motors
hopper = Motor(Ports.PORT2, True)  # half motor
intake_bottom = Motor(Ports.PORT10, GearSetting.RATIO_6_1, False)
intake_top = Motor(Ports.PORT1)  # half motor

# Torque Amounts
front_right.set_max_torque(100, PERCENT)
middle_right.set_max_torque(100, PERCENT)
back_right.set_max_torque(100, PERCENT)
front_left.set_max_torque(100, PERCENT)
middle_left.set_max_torque(100, PERCENT)
back_left.set_max_torque(100, PERCENT)
hopper.set_max_torque(100, PERCENT)
intake_bottom.set_max_torque(100, PERCENT)
intake_top.set_max_torque(100, PERCENT)

# Odometry
# Basic (one-wheel)
# tracking_wheel = Rotation(Ports.PORT14)

# Standard (two-wheel)
parallel_tracking = Rotation(Ports.PORT3)  # parallel to drive wheels
perpendicular_tracking = Rotation(Ports.PORT4)  # perpendicular to drive wheels

# Advanced (three-wheel)
# left_tracking = Rotation(Ports.PORT14)
# right_tracking = Rotation(Ports.PORT15)
# back_tracking = Rotation(Ports.PORT16)

# Sensors
inertial_sensor = Inertial(Ports.PORT16)
optical_sensor = Optical(Ports.PORT6)
gps_sensor = Gps(Ports.PORT17, 0, 0, DistanceUnits.MM, 180)
block_color_sensor = Optical(Ports.PORT8)

# Pneumatics
aligner_out_port = DigitalOut(
    brain.three_wire_port.a
)  # False (0) is piston out, True (1) is piston in
henry = DigitalOut(brain.three_wire_port.b)

controller_1 = Controller(PRIMARY)

# Custom constants

HOPPER_DEGREES_PER_BLOCK = 180

# Currently only DRIVE is implemented.
# Eventually should add INTAKE, HOPPER, etc.
DEBUG_MODES = ["DRIVE"]
