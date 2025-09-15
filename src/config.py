"""
Contains builtin VEX motors and sensors as well as constants.
"""

from vex import *

brain = Brain()

#True = reversed, False = normal

# Drivetrain motors
front_right = Motor(Ports.PORT13, GearSetting.RATIO_6_1, False)
middle_right = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
back_right = Motor(Ports.PORT20, GearSetting.RATIO_6_1, False)
front_left = Motor(Ports.PORT18, GearSetting.RATIO_6_1, True)
middle_left = Motor(Ports.PORT19, GearSetting.RATIO_6_1, True)
back_left = Motor(Ports.PORT11, GearSetting.RATIO_6_1, True)

# Auxillary motors
hopper = Motor(Ports.PORT1)  # half motor
intake_bottom = Motor(Ports.PORT10, GearSetting.RATIO_6_1, False)
intake_top = Motor(Ports.PORT2)  # half motor

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
inertial_sensor = Inertial(Ports.PORT5)
optical_sensor = Optical(Ports.PORT6)
gps_sensor = Gps(Ports.PORT7, 0, 0, DistanceUnits.MM, 180)
block_color_sensor = Optical(Ports.PORT8)

# Tube intake (pneumatic)
henry = DigitalOut(brain.three_wire_port.a)

controller_1 = Controller(PRIMARY)

# Custom constants

HOPPER_DEGREES_PER_BLOCK = 180

# Currently only DRIVE is implemented.
# Eventually should add INTAKE, HOPPER, etc.
DEBUG_MODES = ["DRIVE"]
