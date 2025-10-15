"""
Contains functions relating to the V5 Screen, like the selection screen and logger.
"""

from vex import *


class SelectionButton:
    """
    Initial selection screen buttons.
    """

    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int) -> None:
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def pressed(self, x: int, y: int) -> bool:
        """
        Given an x and y brain screen position, output True if pressed and False if not.
        """
        return (x >= self.x_min and x < self.x_max) and (
            y >= self.y_min and y < self.y_max
        )


class Selection:
    """
    Initial selection screen for autonomous or skills code.
    """

    def __init__(
        self,
        brain: Brain,
        selection_image_path: str,
        buttons: dict[SelectionButton, Callable],  # {SelectionButton, auton function}
    ) -> None:
        self._brain = brain
        self.buttons = buttons

        self._brain.screen.draw_image_from_file(selection_image_path, 0, 0)

    def pressed(self) -> Callable | None:
        """
        Return which button has been pressed, or None.
        """
        x = self._brain.screen.x_position()
        y = self._brain.screen.y_position()

        for button, auton_function in self.buttons.items():
            if button.pressed(x, y):
                return auton_function


class Logger:
    """
    Helper class for printing console-like updates to the V5 Brain screen in a sane way.
    Should be run as a thread. Prints new updates below old ones; scrolls automatically.
    """

    def __init__(self, brain: Brain, lines=12, font=FontType.MONO20) -> None:
        self._brain = brain
        self._print_queue = []
        # This print queue uses nested lists in the format
        # [[module_name, message], [module_name, message]]
        self.max_lines = lines
        self.font = font

        self._next_stop_print = False

    def start_print_loop(self) -> None:
        self._brain.screen.clear_screen()
        while not self._next_stop_print:
            self._print_loop()

            sleep(200)
            # Not the most essential task in the world
            # It's okay if we lose a fifth of a second to CPU scheduling

    def stop_print_loop(self) -> None:
        self._next_stop_print = True

    def _print_loop(self) -> None:
        for col in range(self.max_lines, 0, -1):
            # Prints backwards.
            # Starts at the bottom with the most current messages,
            # then fills any remaining space with old messages.
            self._brain.screen.set_cursor(col, 1)

            if len(self._print_queue) > 0:
                module, message = self._print_queue[
                    -min(col, len(self._print_queue))
                ]  # clamp this
                self._brain.screen.print(module + ": " + message)
                self._print_queue = self._print_queue[:10]

    def log(self, module_name: str, message: str) -> None:
        """
        Queues a message for logging on the V5 Brain.
        """
        self._print_queue.append([module_name, message])


class NullLogger:
    """
    A dummy logger.
    """

    def log(*args, **kwargs) -> None:
        pass

    def start_print_loop(*args, **kwargs) -> None:
        pass
