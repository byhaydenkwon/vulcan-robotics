"""
Contains builtin VEX motors and sensors as well as constants.
"""

from vex import *

brain = Brain()

# Drivetrain motors
front_right = Motor(Ports.PORT1, GearSetting.RATIO_6_1, False)
middle_right = Motor(Ports.PORT2, GearSetting.RATIO_6_1, False)
back_right = Motor(Ports.PORT3, GearSetting.RATIO_6_1, False)
front_left = Motor(Ports.PORT8, GearSetting.RATIO_6_1, True)
middle_left = Motor(Ports.PORT9, GearSetting.RATIO_6_1, True)
back_left = Motor(Ports.PORT10, GearSetting.RATIO_6_1, True)

# Drivetrain torque
front_right.set_max_torque(100, PERCENT)
middle_right.set_max_torque(100, PERCENT)
back_right.set_max_torque(100, PERCENT)
front_left.set_max_torque(100, PERCENT)
middle_left.set_max_torque(100, PERCENT)
back_left.set_max_torque(100, PERCENT)

# Scoring motors (all half motors)
intake_motor = Motor(Ports.PORT5, True)
top_motor = Motor(Ports.PORT21, False)
middle_motor = Motor(Ports.PORT7, False)
hopper_motor = Motor(Ports.PORT11, False)

# Sensors
inertial_sensor = Inertial(Ports.PORT16)

# Pneumatics
aligner_port = DigitalOut(brain.three_wire_port.a)
match_loader_port = DigitalOut(brain.three_wire_port.b)

controller = Controller(PRIMARY)
