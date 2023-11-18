"""Contains tools for interacting with PyAutoGUI"""
import pyautogui
import numpy as np


class System:
    """
    This class provides methods for capturing screenshots and simulating mouse actions.

    Attributes:
        None

    Methods:
        - image(): Take a screenshot.
        - mouse(dataPoint, clicks): Move the mouse pointer to specified
          screen coordinates and perform the given number of mouse clicks.

    Notes:
        This class only uses the PyAutoGUI library for system interactions.
        Please refer to the README for KeyFlare the latest installation instructions.

    Example:
        >>> system = System()
        >>> screenshot = system.image()
        >>> print(screenshot.shape)  # Output: (screen_height, screen_width, 3)
        >>> dataPoint = (500, 300)  # Example screen coordinates
        >>> system.mouse(dataPoint)  # Performs a single left-click at (500, 300)
    """

    def image(self):
        """
        Take a screenshot without your mouse in the image.

        Returns:
            np.ndarray: A NumPy array representing the screenshot image.

        Notes:
            This method uses the `pyautogui.screenshot()` function
            to capture a screenshot of the entire current screen.
            PyAutoGUI has a number of system requirements that differ depending on the OS.
            Please check the README for the latest installation instructions for KeyFlare.

        Example:
            >>> system = System()
            >>> screenshot = system.image()
            >>> print(screenshot.shape)  # Output: (screen_height, screen_width, 3)
        """
        screenshot = pyautogui.screenshot()
        return np.array(screenshot)

    def mouse(self, datapoint, clicks=1, button="left", scroll_distance=None):
        """
        Moves the mouse pointer to a specified screen coordinate,
        performs a number of clicks (left or right), and scrolls by a specified distance.

        Args:
            dataPoint (tuple or list, required):
                A tuple or list representing the target screen coordinates (x, y).
            clicks (int, optional): The number of mouse clicks to perform (default is 1).
            button (str, optional): The mouse button to use ('left' or 'right', default is 'left').
            scroll_distance (int or float, optional):
                The distance to scroll the mouse wheel. Positive values scroll up, negatives down.

        Returns:
            None

        Notes:
            Uses the `pyautogui.moveTo()`, `pyautogui.click()`, and `pyautogui.scroll()`.
            Again, PyAutoGUI has a number of varying system requirements.
            Please check the README for the latest installation instructions for KeyFlare.

        Example:
            >>> system = System()
            >>> dataPoint = (500, 300)  # 500 right, 300 down of the top-right corner of the screen.
            >>> system.mouse(dataPoint)  # Performs a single left-click at (500, 300)
            >>> system.mouse(dataPoint, button='right')  # Performs a right-click at (500, 300)
            >>> system.mouse(dataPoint, scroll_distance=3)  # Scrolls up by 3 units
        """
        pyautogui.moveTo(datapoint[0], datapoint[1])
        if button == "left":
            pyautogui.click(clicks=clicks)
        elif button == "right":
            pyautogui.click(clicks=clicks, button=pyautogui.RIGHT)
        # Scroll is not used yet, but is implemented
        if scroll_distance is not None:
            pyautogui.scroll(scroll_distance)
