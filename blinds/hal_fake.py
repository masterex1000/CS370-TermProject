# This is a hal that simulates fake hardware. It'll randomly toggle
# the light on and off, and will print debug output saying when the 
# blinds are open/closed

import time

class BlindHal:
    """A fake hal for testing the project"""

    lightState = False

    def __init__(self):
        pass

    def isLight(self) -> bool:
        # Toggle every 10 seconds
        return (time.time() % 20) > 10

    def setOpen(self, state : bool):
        print("Blind state set to ", state)
