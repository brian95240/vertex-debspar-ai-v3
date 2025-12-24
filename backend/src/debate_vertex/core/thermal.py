from enum import Enum

class ThermalTier(Enum):
    HOT = 3      # Always resident (Orchestrator)
    WARM = 2     # Pilot Light (Local 7B Model)
    COLD = 1     # Full spin-up (Not used in Hybrid)

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented