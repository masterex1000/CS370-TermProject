from collections import namedtuple
from enum import Enum


BlindEvent = namedtuple('BlindEvent', ['name', 'value'])

# type : BlindValueId # Which value is being changed
BlindEventChangeValue = namedtuple('BlindEventChangeValue', ['type', 'value'])

class BlindEventType(Enum):
    DEBUG_PRINT = 1
    VALUE_UPDATE = 2 # associated with some sort of value being modified (uses BlindEventChangeValue as value) 

class BlindValueId(Enum):
    time = 1
    motion = 2
    light = 3
    override = 4
    override_state = 5
    output_state = 6
