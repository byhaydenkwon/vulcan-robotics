# no enum library :(
class ScoringStates:
    OFF = "OFF"
    INTAKING = "INTAKING"
    SCORING_LOW = "SCORING_LOW"
    SCORING_MIDDLE = "SCORING_MIDDLE"
    SCORING_HIGH = "SCORING_HIGH"
    FLUSHING = "FLUSHING"
    JAMMED = "JAMMED"  # not currently used


# This is a workaround for type hints. Since there's no Enum class available,
# we can't just type hint IntakeState (because it's not an enum!)
# Instead, just type hint IntakeStateValue.
ScoringStateValue = str


class ScoringTargets:
    INTAKE = "INTAKE"
    LOW = "LOW"
    MIDDLE = "MIDDLE"
    HIGH = "HIGH"
    FLUSH = "FLUSH"


ScoringTargetValue = str
