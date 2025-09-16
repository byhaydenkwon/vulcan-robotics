from vex import *

"""
The skills/driver control selection screen.
"""

class Selection:
    def __init__(self, brain: Brain, image_path: str):
        self.image_path = image_path
        self.brain = brain

        self.brain.screen.draw_image_from_file(self.image_path, 0, 0)

class SelectionButton:
    def __init__(self, start_x: int, start_y: int, end_x: int, end_y: int) -> None:
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = start_x
        self.end_y = end_y  
