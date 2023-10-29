"""
Re-export builtins that panda3d created for readability
"""

import builtins

def __getattr__(name):
    return getattr(builtins, name)
