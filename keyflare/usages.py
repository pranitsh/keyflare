"""Determines the best way to run the module"""
import time
import sys
import platform
from .gui import GUI

try:
    from pynput import keyboard
except ImportError:
    import logger

    logger.info("Could not create shortcuts.")


class Usages:
    """
    This class determines the way to use keyflare if called through main,
    whether it is __main__, main(), or maybe something else in the future.

    Attributes:
        args (list): Command-line arguments passed to the program.
        platf (str): The platform (e.g., 'Windows',
        'Linux', 'Darwin') on which the program is running.
        z (GUI): An instance of the GUI class.
        clicks (int, defaults to 1): The number of clicks
        to perform when a keyboard shortcut is triggered.

    Methods:
        __init__(): Initializes the Usages class and sets up necessary attributes.
        runType(): Calls the shortcut method to listen for keyboard shortcuts.
        shortcut(): Listens for specific keyboard shortcuts and triggers GUI actions accordingly.
        programmatic(): Executes GUI actions programmatically based on command-line arguments.

    Notes:
        - This class depends on the external
          library 'pynput' and standard library 'platform'.
        - It is designed to work with a GUI application represented by the 'GUI' class.
        - The keyboard shortcuts are defined
          in the 'start_combination' list. The chosen shortcut is alt+A.

    Examples:
        >>> usage = Usages()
        >>> usage.runType()
    """

    args = None
    platf = None
    z = None
    clicks = 1

    def __init__(self):
        """
        Initializes the Usages class.

        Args:
            None

        Returns:
            None
        """
        self.args = sys.argv
        self.platf = platform.system()
        self.z = GUI()
        self.runtype()

    def runtype(self):
        """
        Uses the number of args to determine how to run.

        Args:
            None

        Returns:
            None

        Note:
            If there are multiple args, uses programmatic control.
            If there are no args, uses keyboard shortcuts to activate.s
        """
        if len(self.args) > 1:
            self.programmatic()
        else:
            self.shortcut()

    def shortcut(self):
        """
        Listens for keyboard shortcuts and triggers the GUI action if the shortcut is pressed.

        Args:
            None

        Returns:
            None

        Notes:
            - This method relies on `pynput`, which has platform
              specific limitations. Please read the README for bypassing them.
        """
        print("[KeyFlare] Press (left Alt)+(lowercase a) to activate.")
        print("[KeyFlare] Perform a keyboard interrupt to exit.")
        start_combination = [
            {keyboard.Key.alt, keyboard.KeyCode(char="a")},
            {keyboard.Key.alt_l, keyboard.KeyCode(char="a")},
            {keyboard.Key.alt, keyboard.KeyCode(char="s")},
            {keyboard.Key.alt_l, keyboard.KeyCode(char="s")},
        ]
        current = set()

        def on_press(key):
            if any([key in COMBO for COMBO in start_combination]):
                current.add(key)
                if len(current) == 2:
                    if keyboard.KeyCode(char="s") in current:
                        self.z.run(clicks=self.clicks, button="right")
                        current.clear()
                    else:
                        self.z.run(clicks=self.clicks, button="left")
                        current.clear()

        def on_release(key):
            if any([key in COMBO for COMBO in start_combination]):
                try:
                    current.remove(key)
                except KeyError:
                    pass

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

        try:
            while not self.z.exit_flag:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("Exiting the application.")
            listener.stop()
        else:
            listener.stop()

    def programmatic(self):
        """
        Executes GUI actions programmatically based on command-line arguments.

        Args:
            None

        Returns:
            None

        Notes:
            - This method is typically called from the command
              line with the desired number of clicks and the button as the argument.

        Examples:
            ```sh
            keyflare 3 left
            ```
        """
        print("[Usages] Using commandline keyflare.")
        self.z.run(clicks=int(self.args[1]), button=str(self.args[2]))


def main():
    """
    The main entry point of the script.

    Args:
        None

    Returns:
        None
    """
    Usages()


if __name__ == "__main__":
    main()
