"""
Re-export builtins that panda3d created for readability
"""

import builtins
from typing import Any


def __getattr__(name: Any):
    return getattr(builtins, name)
