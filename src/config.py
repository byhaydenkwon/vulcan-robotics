"""
Contains builtin VEX motors and sensors as well as constants.
"""

from vex import *

brain = Brain()

#True = reversed, False = normal

# Drivetrain motors
front_right = Motor(Ports.PORT1, GearSetting.RATIO_6_1, False)
middle_right = Motor(Ports.PORT2, GearSetting.RATIO_6_1, False)
back_right = Motor(Ports.PORT3, GearSetting.RATIO_6_1, False)
front_left = Motor(Ports.PORT4, GearSetting.RATIO_6_1, True)
middle_left = Motor(Ports.PORT5, GearSetting.RATIO_6_1, True)
back_left = Motor(Ports.PORT6, GearSetting.RATIO_6_1, True)

# Auxillary motors
hopper = Motor(Ports.PORT11, True)  # half motor
intake_bottom = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
intake_top = Motor(Ports.PORT13, True)  # half motor

# Odometry
# Basic (one-wheel)
# tracking_wheel = Rotation(Ports.PORT14)

# Standard (two-wheel)
parallel_tracking = Rotation(Ports.PORT14)  # parallel to drive wheels
perpendicular_tracking = Rotation(Ports.PORT15)  # perpendicular to drive wheels

# Advanced (three-wheel)
# left_tracking = Rotation(Ports.PORT14)
# right_tracking = Rotation(Ports.PORT15)
# back_tracking = Rotation(Ports.PORT16)

# Sensors
inertial_sensor = Inertial(Ports.PORT7)
optical_sensor = Optical(Ports.PORT8)
gps_sensor = Gps(Ports.PORT9, 0, 0, DistanceUnits.MM, 180)
block_color_sensor = Optical(Ports.PORT10)

# Tube intake (pneumatic)
henry = DigitalOut(brain.three_wire_port.a)

controller_1 = Controller(PRIMARY)

# Custom constants

HOPPER_DEGREES_PER_BLOCK = 180

# Currently only DRIVE is implemented.
# Eventually should add INTAKE, HOPPER, etc.
DEBUG_MODES = ["DRIVE"]
