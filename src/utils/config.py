"""
Contains builtin VEX motors and sensors as well as constants.
"""

from vex import *

brain = Brain()

# Drivetrain motors
right_1 = Motor(Ports.PORT11, GearSetting.RATIO_6_1, False)
right_2 = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
right_3 = Motor(Ports.PORT13, GearSetting.RATIO_6_1, True)
left_1 = Motor(Ports.PORT14, GearSetting.RATIO_6_1, True)
left_2 = Motor(Ports.PORT15, GearSetting.RATIO_6_1, True)
left_3 = Motor(Ports.PORT16, GearSetting.RATIO_6_1, False)

# Drivetrain torque
right_1.set_max_torque(100, PERCENT)
right_2.set_max_torque(100, PERCENT)
right_3.set_max_torque(100, PERCENT)
left_1.set_max_torque(100, PERCENT)
left_2.set_max_torque(100, PERCENT)
left_3.set_max_torque(100, PERCENT)

# Scoring motors (all half motors)
intake_motor = Motor(Ports.PORT1, True)
top_motor = Motor(Ports.PORT3, True)
middle_motor = Motor(Ports.PORT10, True)
hopper_motor = Motor(Ports.PORT2, True)

# Sensors
inertial_sensor = Inertial(Ports.PORT17)

# Pneumatics
aligner_port = DigitalOut(brain.three_wire_port.a)
match_loader_port = DigitalOut(brain.three_wire_port.b)

controller = Controller(PRIMARY)

# Code configuration
# Data types are intentionally provided for easier configuration
DRIVETRAIN_GEAR_RATIO: float = 0.625
DRIVETRAIN_WHEEL_DIAMETER: float = 3.25

DRIVER_VELOCITY: float = 100.00
DRIVER_TURN_VELOCITY: float = 69.42067

AUTO_SELECTION_IMAGE: str = "images/vulcan-selection-screen.png"
AUTO_WP_SELECTION_IMAGE: str = "images/vulcan-wp-selection-screen.png"
