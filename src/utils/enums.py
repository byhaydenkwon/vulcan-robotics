# no enum library :(
class IntakeStates:
    OFF = "OFF"
    INTAKING = "INTAKING"
    OUTTAKING_LOW = "OUTTAKING_LOW"
    OUTTAKING_MIDDLE = "OUTTAKING_MIDDLE"
    OUTTAKING_HIGH = "OUTTAKING_HIGH"
    JAMMED = "JAMMED"  # not currently used


# This is a workaround for type hints. Since there's no Enum class available,
# we can't just type hint IntakeState (because it's not an enum!)
# Instead, just type hint IntakeStateValue.
IntakeStateValue = str


class IntakeTargets:
    INTAKE = "INTAKE"
    LOW = "LOW"
    MIDDLE = "MIDDLE"
    HIGH = "HIGH"


IntakeTargetValue = str
