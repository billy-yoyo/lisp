from .core import NATIVES as CORE_NATIVES
from .std import NATIVES as STD_NATIVES
from .math import NATIVES as MATH_NATIVES
from .data import NATIVES as DATA_NATIVES

NATIVES = {}
NATIVES.update(CORE_NATIVES)
NATIVES.update(STD_NATIVES)
NATIVES.update(MATH_NATIVES)
NATIVES.update(DATA_NATIVES)
