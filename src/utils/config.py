"""
Contains builtin VEX motors and sensors as well as constants.
"""

from vex import *

brain = Brain()

# Drivetrain motors
front_right = Motor(Ports.PORT13, GearSetting.RATIO_6_1, False)
middle_right = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
back_right = Motor(Ports.PORT20, GearSetting.RATIO_6_1, False)
front_left = Motor(Ports.PORT18, GearSetting.RATIO_6_1, True)
middle_left = Motor(Ports.PORT19, GearSetting.RATIO_6_1, True)
back_left = Motor(Ports.PORT11, GearSetting.RATIO_6_1, True)

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

# Sensors
inertial_sensor = Inertial(Ports.PORT16)

# Pneumatics
aligner_port = DigitalOut(brain.three_wire_port.a)
match_loader_port = DigitalOut(brain.three_wire_port.b)

controller_1 = Controller(PRIMARY)
