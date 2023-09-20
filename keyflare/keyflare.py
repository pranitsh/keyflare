#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import tkinter.colorchooser as cc
import numpy as np
import pyautogui
import time
import cv2
from rtree import index
import sys
import tempfile
import platform

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

class ImagePipeline:
    """
    The `ImagePipeline` class performs a series of image processing tasks on a screenshot captured by the `System` class. It extracts coordinates of possibly clickable areas, removes overlapping bounding boxes, and labels the remaining boxes alphabetically. The processed data can then be used for various purposes, such as creating a graphical user interface (GUI) for navigating with your computer!

    Attributes:
        original_image (None): A placeholder for the original screenshot image.
        coordinate_data (list): A list to store coordinate data, including bounding boxes of clickable areas.
        x (System): An instance of the `System` class used for capturing screenshots.

    Methods:
        - run(): Executes the image processing pipeline.
        - processing_image(): Extracts contours from the original image into the coordinate_data.
        - processing_data(): Processes coordinate data to remove overlapping boxes and label the remaining boxes, recycling coordinate_data.

    Notes:
        - The `ImagePipeline` class relies on the `System` class for capturing the original screenshot.
        - The processed results can be accessed using the `coordinate_data` attribute.

    Example:
        >>> pipeline = ImagePipeline()
        >>> pipeline.run()  # Executes the image processing pipeline
        >>> coordinate_data = pipeline.coordinate_data
        >>> print(len(coordinate_data))  # Output: Number of labeled bounding boxes
    """
    original_image = None
    coordinate_data = list()
    x = System()
    
    def run(self):
        """
        Executes the image processing pipeline. This method starts the image processing pipeline after taking a screenshot. The results are stored in the class as an attribute, which is then displayed through the GUI class.

        Args:
            None

        Returns:
            None

        Notes:
            - The method relies on the `System` class for capturing the original image.
            - The processed results can be accessed using the class's attributes.

        Example:
            >>> pipeline = ImagePipeline()
            >>> pipeline.run()
            >>> coordinate_data = pipeline.coordinate_data
            >>> print(len(coordinate_data))  # Output: Number of clickable places found
        """
        self.coordinate_data = list()
        self.original_image = self.x.image()
        self.processing_image()
        self.processing_data()

    def processing_image(self):
        """
        Processes the original image to extract contours into coordinate data. After converting an image from grey to black and white with adapative thresholding, the use of morpohological operations expands bright spots and contracts dark spots. The results, the contours of the image with and without morphological operations, are stored combined for further processing.

        Args:
            None

        Returns:
            None

        Notes:
            - This method is a part of the image processing pipeline.
            - It uses OpenCV (cv2) functions for image manipulation.
            - The results are stored in the class's `coordinate_data`.

        Example:
            >>> pipeline = ImagePipeline()
            >>> pipeline.run()  # Executes the image processing pipeline
            >>> original_contours = pipeline.original_contours
            >>> processed_contours = pipeline.processed_contours
            >>> coordinate_data = pipeline.coordinate_data
            >>> print(len(coordinate_data))  # Output: Number of extracted bounding boxes
        """
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
        threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        original_contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        kernel = np.ones((1, 4), np.uint8)
        dilated = cv2.dilate(threshold, kernel, iterations=1)
        processed_contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in processed_contours:
            x, y, w, h = cv2.boundingRect(cnt)
            self.coordinate_data.append([x, y, w, h])
        for cnt in original_contours:
            x, y, w, h = cv2.boundingRect(cnt)
            self.coordinate_data.append([x, y, w, h])

    def processing_data(self):
        """
        Process the coordinate data to remove overlapping boxes and label the remaining boxes.

        This method processes the coordinate data extracted from the image processing step. It includes the following steps:
        1. Index the coordinate_data, which technically holds bounding boxes before this step, into the R-tree spatial indexing algorithm.
        2. Remove overlapping bounding boxes.
        3. Labeling the remaining bounding boxes alphabetically.

        Args:
            None

        Returns:
            None

        Notes:
            - It uses the R-tree spatial index for efficient data manipulation.
            - This method is a part of the image processing pipeline.
            - The results are stored in the class's `coordinate_data` attribute.

        Example:
            >>> pipeline = ImagePipeline()
            >>> pipeline.run()  # Executes the image processing pipeline
            >>> coordinate_data = pipeline.coordinate_data
            >>> print(len(coordinate_data))  # Output: Number of labeled bounding boxes
            
        Further Improvements:
            - Currently, if an item is overlapping another bounding box by 10 pixels on any side of the box, it is added to a list to be removed. An adaptive method designed to get a specific number of boxes would work better.
        """
        properties = index.Property()
        properties.dimension = 2
        properties.dat_extension = 'data'
        properties.idx_extension = 'index'
        properties.buffering_capacity = 200
        properties.pagesize = 8192
        properties.node_capacity = 100
        properties.leaf_capacity = 100
        properties.fill_factor = 0.1
        rt = index.Index(properties=properties)
        boxes_to_remove = set()
        for i, data_point in enumerate(self.coordinate_data):
            if data_point[2] * data_point[3] > 15:
                rt.insert(i, (data_point[0], data_point[1], data_point[0]+data_point[2], data_point[1]+data_point[3]))
        for i in rt.intersection((float('-inf'), float('-inf'), float('inf'), float('inf'))):
            if i not in boxes_to_remove:
                intersectingIndices = list(rt.intersection(
                    (self.coordinate_data[i][0]-10, self.coordinate_data[i][1]-10, self.coordinate_data[i][0]+self.coordinate_data[i][2]+10, self.coordinate_data[i][1]+self.coordinate_data[i][3]+10)))
                if len(intersectingIndices) > 1:
                    for j in intersectingIndices:
                        if i != j:
                            if (self.coordinate_data[i][2]*self.coordinate_data[i][3]) <= self.coordinate_data[j][2]*self.coordinate_data[j][3] - 5:
                                boxes_to_remove.add(j)
        for i in boxes_to_remove:
            rt.delete(i, (self.coordinate_data[i][0], self.coordinate_data[i][1], self.coordinate_data[i][0] + self.coordinate_data[i][2], self.coordinate_data[i][1]+self.coordinate_data[i][3]))
        allItems = list()
        for item in rt.intersection((float('-inf'), float('-inf'), float('inf'), float('inf'))):
            allItems.append(self.coordinate_data[item])
        self.coordinate_data = allItems
        length = 1
        current_string = ""
        alphabet_strings = []
        while True:
            for letter in "etaoinsrhlcdumfpwybgvkxjqz":
                alphabet_strings.append(current_string + letter)
                if len(alphabet_strings) == len(self.coordinate_data):
                    break
            if len(alphabet_strings) == len(self.coordinate_data):
                break
            current_string += letter
            length += 1

        toMap = [[item[0], item[1], item[2], item[3]] for item in self.coordinate_data]
        self.coordinate_data = list(zip(alphabet_strings, toMap))

class GUI:
    """
    This class named GUI (Graphical User Interface) serves as the primary interface for interacting with KeyFlare. It includes a coordinate selector, a keyboard input detector, color selector, etc. It continuously narrows down the location of your intended mouse click until it has been resolved, clicking automatically without a mouse.

    Attributes:
        root (Tk object): The root Tk window for the KeyFlare application.
        input_char (str): The character input by the user.
        y (ImagePipeline object): An instance of the ImagePipeline class used for image processing and coordinate finding.
        exit_flag (bool): Flag to indicate whether to exit the application or not by the Usages class.
        color (tuple): The selected input method's color represented in (R, G, B) format.
        label: A tk Label to be shown in the application.
        temp_name: Name of the temporary file.

    Methods:
        run(clicks: int): Runs KeyFlare's GUI process for selecting a coordinate.
        selecting_coordinate(clicks: int): Manages the process of selecting a coordinate on the keyboard image.
        on_key(event): Filters and updates available key options on a keyboard input.
        exit_app(): Gracefully exits the KeyFlare application.
        select_color(): Opens a color selection dialog and updates the selected color in the GUI.
        rgb_to_hex(rgb: tuple): Converts an RGB color tuple to its hexadecimal representation.
        focus_window(): Sets the application window to the foreground and ensures it has focus.
    """
    root = None
    input_char = ""
    y = ImagePipeline()
    exit_flag = False
    color = (248, 93, 94)
    label = None
    temp_name = None

    def run(self, clicks):
        """
        Runs KeyFlare's graphical user interface process for selecting a coordinate.

        Args:
            clicks (int, required): The number of mouse clicks to perform when a place to click has been found.

        Returns:
            None

        Notes:
            - Users can press a key on their physical keyboard, and the GUI will respond by narrowing down the available key options based on the input character.
            - If no matching key is found, the GUI will display color selection options and allow the user to exit the application.

        Example:
            >>> gui = GUI()
            >>> gui.run(clicks=2)
        """
        self.y.run()
        self.root = tk.Tk()
        self.root.title("KeyFlare")
        self.root.wm_attributes('-fullscreen', True)
        self.root.attributes('-topmost', 1)
        self.root.focus_force()
        self.label = tk.Label().pack()
        self.selecting_coordinate(clicks)

    def selecting_coordinate(self, clicks):
        """
        Manages the process of selecting a coordinate on the keyboard image, clicking the point at the end or showing a preference menu at the end if no point was found.

        Args:
            clicks (int, required): The number of mouse clicks to perform when a place to click has been found.

        Returns:
            None

        Example:
            >>> gui = GUI()
            >>> gui.run(clicks=2) # Notice: please do not run this by itself
        """
        for i in range(6):
            image = self.y.original_image.copy()
            if self.label:
                self.label.destroy()
            if self.root.winfo_exists():
                for key, loc in self.y.coordinate_data:
                    image = cv2.rectangle(image, (loc[0], loc[1]), (loc[0] + 13 * len(self.y.coordinate_data[0][0]), loc[1] + 20), self.color, -1)
                    text_size, _ = cv2.getTextSize(key, cv2.FONT_HERSHEY_PLAIN, 0.75, 1)
                    image = cv2.putText(image, key, (loc[0] + (10 * len(self.y.coordinate_data[0][0]) - text_size[0]) // 2, loc[1] + (20 + text_size[1]) // 2), \
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (0, 0, 0), 1, cv2.LINE_AA)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                _, buffer = cv2.imencode(".png", image)
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                    temp_file.write(buffer.tobytes())
                    self.temp_name = temp_file.name
                image = tk.PhotoImage(file=self.temp_name)
                self.label = ttk.Label(self.root, image=image)
                self.label.pack()
                self.root.update_idletasks()
                self.root.lift()
                self.root.focus_force()
                self.root.after(1, lambda: self.root.focus_force())
                self.root.attributes('-topmost', True)
                self.root.after_idle(self.root.attributes, '-topmost', False)
                self.root.focus_force()
                self.root.after(50, self.focus_window)
                self.root.bind("<Key>", self.on_key)
                self.root.grab_set()
                self.root.mainloop()
            if len(self.y.coordinate_data) == 1:
                self.root.destroy()
                self.y.x.mouse([self.y.coordinate_data[0][1][0]+10, self.y.coordinate_data[0][1][1]+10], clicks=clicks)
                break
            elif len(self.y.coordinate_data) == 0:
                self.root.quit()
                self.label.destroy()
                style = ttk.Style()
                style.theme_use("classic")
                label_frame = ttk.Frame(self.root, padding=20)
                label_frame.pack(fill="both", expand=True)
                self.label = ttk.Label(label_frame, text="Selected color:", font=("Arial", 14), background=self.rgb_to_hex(self.color), foreground="#000000")
                self.label.pack()
                select_button = ttk.Button(self.root, text="Select Color", command=self.select_color)
                select_button.pack(pady=10)
                exit_button = ttk.Button(self.root, text="Completely Exit KeyFlare", command=self.exit_app)
                exit_button.pack(pady=10)
                pass_button = ttk.Button(self.root, text="Continue (or Press Any Key)", command=self.root.destroy)
                pass_button.pack(pady=10)
                self.root.bind("<Key>", lambda e: self.root.destroy())
                self.root.mainloop()
                break

    def on_key(self, event):
        """
        Filters and updates available key options on a keyboard input event. Narrows down the choices to find the spot to click.

        Args:
            event (tkinter.Event): The keyboard event containing information about the pressed key.

        Returns:
            None

        Example:
            To use this method, you can define it as an event handler for a tkinter window like this:
            >>> self.root.bind("<Key>", self.on_key)
        """
        self.input_char = event.char
        self.y.coordinate_data = [(key[len(self.input_char):], p1) for key, p1 in self.y.coordinate_data if key[0].lower() == self.input_char.lower()]
        self.root.quit()

    def exit_app(self):
        """
        For exiting the KeyFlare application gracefully. It sets an exit flag and closes the application window.

        Args:
            None

        Returns:
            None

        Example:
            >>> gui = GUI()
            >>> gui.exit_app()
        """
        self.exit_flag = True
        self.root.destroy()

    def select_color(self):
        """
        Opens a color selection dialog and updates the selected color in the GUI. The selected color is then displayed in the GUI, and the RGB values are updated.

        Args:
            None

        Returns:
            None

        Example:
            >>> gui = GUI()
            >>> gui.run()
            >>> gui.select_color()
        """
        color = cc.askcolor()[1]
        if color:
            if isinstance(color, str) and color.startswith('#'):
                color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            self.color = tuple(map(int, color))
            self.label.config(text=f"Selected color: {self.color}", background=self.rgb_to_hex(self.color))

    def rgb_to_hex(self, rgb):
        """
        Converts an RGB color tuple to its hexadecimal representation.

        Args:
            rgb (tuple): A tuple containing three integers representing the red, green, and blue color channels, respectively.

        Returns:
            str: The hexadecimal representation of the RGB color.

        Example:
            >>> gui = GUI()
            >>> color_tuple = (255, 0, 128)
            >>> hex_color = gui.rgb_to_hex(color_tuple)
            >>> print(hex_color)
            "#FF0080"
        """
        r, g, b = rgb
        return f"#{r:02x}{g:02x}{b:02x}"

    def focus_window(self):
        """
        Sets the application window to the foreground and ensures it has focus, no matter what. It is against the purpose of the application to find you have to use your mouse to click the image shown.

        Args:
            None

        Returns:
            None

        Example:
            >>> gui = GUI()
            >>> gui.run()
            >>> gui.focus_window()
        """
        self.root.lift()
        self.root.focus_force()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        self.root.focus_force()

class Usages:
    """
    This class determines the way to use keyflare if called through main, whether it is __main__, main(), or maybe something else in the future.

    Attributes:
        args (list): Command-line arguments passed to the program.
        platf (str): The platform (e.g., 'Windows', 'Linux', 'Darwin') on which the program is running.
        z (GUI): An instance of the GUI class.
        clicks (int, defaults to 1): The number of clicks to perform when a keyboard shortcut is triggered.

    Methods:
        __init__(): Initializes the Usages class and sets up necessary attributes.
        runType(): Calls the shortcut method to listen for keyboard shortcuts.
        shortcut(): Listens for specific keyboard shortcuts and triggers GUI actions accordingly.
        programmatic(): Executes GUI actions programmatically based on command-line arguments.

    Notes:
        - This class depends on the external library 'pynput' and standard library 'platform'.
        - It is designed to work with a GUI application represented by the 'GUI' class.
        - The keyboard shortcuts are defined in the 'start_combination' list. The chosen shortcut is alt+A.

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
        self.runType()

    def runType(self):
        """
        Currently unimplemented. Always runs `self.shortcut()`. In the future, this will call the appropriate method.

        Args:
            None

        Returns:
            None
        """
        self.shortcut()
        
    def shortcut(self):
        """
        Listens for keyboard shortcuts and triggers the GUI action if the shortcut is pressed.

        Args:
            None

        Returns:
            None

        Notes:
            - This method relies on `pynput`, which has platform specific limitations. Please read the README for bypassing them.
        """
        from pynput import keyboard
        start_combination = [
            {keyboard.Key.alt_l, keyboard.KeyCode(char='a')},
            {keyboard.Key.alt_r, keyboard.KeyCode(char='a')}
        ]
        current = set()
        
        def on_press(key):
            if any([key in COMBO for COMBO in start_combination]):
                current.add(key)
                if any(all(k in current for k in COMBO) for COMBO in start_combination):
                    self.z.run(clicks=self.clicks)
                    current.clear()
                        
        def on_release(key):
            if any([key in COMBO for COMBO in start_combination]):
                try:
                    current.remove(key)
                except:
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
            - This method is typically called from the command line with the desired number of clicks as an argument.

        Examples:
            ```sh
            python script.py 3
            ```
        """
        print("[Usages] Using commandline keyflare.")
        self.z.run(clicks=int(self.args[1]))

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