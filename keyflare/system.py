import pyautogui
import numpy as np

class System:
    """
    This class provides methods for capturing screenshots and simulating mouse actions.

    Attributes:
        None

    Methods:
        - image(): Take a screenshot.
        - mouse(dataPoint, clicks): Move the mouse pointer to specified screen coordinates and perform the given number of mouse clicks.

    Notes:
        This class only uses the PyAutoGUI library for system interactions. Please refer
        to the README for KeyFlare the latest installation instructions and for bypassing any potential OS limitations for full compatibility.

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
            This method uses the `pyautogui.screenshot()` function to capture a screenshot of the entire current screen.
            PyAutoGUI has a number of system requirements that differ depending on the OS. Please check the README for the latest installation instructions for KeyFlare.

        Example:
            >>> system = System()
            >>> screenshot = system.image()
            >>> print(screenshot.shape)  # Output: (screen_height, screen_width, 3)
        """
        screenshot = pyautogui.screenshot()
        return np.array(screenshot)

    def mouse(self, dataPoint, clicks):
        """
        Moves the mouse pointer to a specified screen coordinate and then performs a number of clicks.

        Args:
            dataPoint (tuple or list, required): A tuple or list representing the target screen coordinates (x, y).
            clicks (int, required): The number of mouse clicks to perform.

        Returns:
            None

        Notes:
            This method uses the `pyautogui.moveTo()` and `pyautogui.click()` functions to perform these mouse actions.
            Again, PyAutoGUI has a number of system requirements that differ depending on the OS. Please check the README for the latest installation instructions for KeyFlare.

        Example:
            >>> system = System()
            >>> dataPoint = (500, 300)  # Example screen coordinates at 500 right and 300 down of the top-right corner of the screen.
            >>> system.mouse(dataPoint)  # Performs a single left-click at (500, 300)
        """
        pyautogui.moveTo(dataPoint[0], dataPoint[1])
        pyautogui.click(clicks=clicks)
