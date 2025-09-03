from vex import *


class Logger:
    """
    Helper class for printing console-like updates to the V5 Brain screen in a sane way.
    Should be run as a thread. Prints new updates below old ones; scrolls automatically.
    """

    def __init__(self, brain: Brain, lines=10, font=FontType.MONO40) -> None:
        self._brain = brain
        self._print_queue = []
        # This print queue uses nested lists in the format
        # [[module_name, message], [module_name, message]]
        self.max_lines = lines
        self.font = font

        self._past_print_queue = []
        self._current_line = 1
        self._next_stop_print = False

    def start_print_loop(self) -> None:
        while not self._next_stop_print:
            self._print_loop()

            sleep(200)
            # Not the most essential task in the world
            # It's okay if we lose a fifth of a second to CPU scheduling

    def stop_print_loop(self) -> None:
        self._next_stop_print = True

    def _print_loop(self) -> None:
        for col in range(self.max_lines, 1, -1):
            # Prints backwards.
            # Starts at the bottom with the most current messages,
            # then fills any remaining space with old messages.
            self._brain.screen.set_cursor(1, col)

            if len(self._print_queue) > 0:
                module, message = self._print_queue[-1]
                self._brain.screen.print(f"{module}: {message}")
                self._past_print_queue.append([module, message])
                self._print_queue.pop()

                if len(self._past_print_queue) >= 10:
                    self._past_print_queue = self._past_print_queue[:10]
                continue

            if len(self._past_print_queue) > 0:
                module, message = self._past_print_queue[-1]
                self._brain.screen.print(f"{module}: {message}")
                continue

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
