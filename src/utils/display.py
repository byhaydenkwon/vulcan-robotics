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
    A singular selection screen that takes SelectionButtons and Callables.
    """

    def __init__(
        self,
        selection_image_path: str,
        buttons: dict[SelectionButton, Callable],  # {SelectionButton: auton function}
    ) -> None:
        self.buttons = buttons

        self.image_path = selection_image_path
        # NOTE Image sizes should be 480x240. Top 32 lines are taken
        # for the V5 status bar; see
        # https://www.vexforum.com/t/introducing-a-new-way-to-display-images-on-your-vex-v5-brain-no-micro-sd-card-required/121687/2

    def pressed(self, x: int, y: int) -> Callable | None:
        """
        Return which button has been pressed, or None.
        """

        for button, auton_function in self.buttons.items():
            if button.pressed(x, y):
                return auton_function


class UserInterface:
    """
    A V5 Brain Screen user interface lifecycle taking multiple Selections in sequence.
    """

    def __init__(
        self,
        brain: Brain,
        selections: dict[str, Selection],
        confirm_image_path: str | None = None,
    ) -> None:
        self.brain = brain
        self.selections = selections
        self.confirm_image_path = confirm_image_path

        self.results: dict[str, Callable | None] = {
            label: None for label in self.selections.keys()
        }
        self.done = False

        self._next_stop_control = False

    def start_ui_loop(self) -> None:
        """
        Waits for input on each selection screen, then moves on to the next one.
        """
        for label, selection in self.selections.items():
            if self._next_stop_control:
                break

            self.brain.screen.draw_image_from_file(selection.image_path, 0, 32)
            while not self._next_stop_control:
                if self.brain.screen.pressing():
                    self.results[label] = selection.pressed(
                        self.brain.screen.x_position(), self.brain.screen.y_position()
                    )
                    self._next_stop_control = True
                wait(200, MSEC)

        if self.confirm_image_path:
            self.brain.screen.draw_image_from_file(self.confirm_image_path, 0, 32)
        else:
            self.brain.screen.clear_screen(Color.GREEN)

        self.done = True

    def stop_ui_loop(self) -> None:
        """
        Prematurely stops the UI loop.
        """
        self._next_stop_control = True

    def get_ui_selection_results(self) -> dict[str, Callable | None]:
        """
        Returns current state of UI selection results.
        Is only complete if UserInterface.done is True.
        """
        return self.results


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
