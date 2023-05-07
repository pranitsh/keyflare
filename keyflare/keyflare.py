#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import tkinter.colorchooser as cc
from ttkthemes import ThemedStyle
import numpy as np
import pyautogui
import time
import cv2
from rtree import index
import pathlib
import sys
import tempfile
from pynput import keyboard

class system:
    """
    A class to manage files and directories, create a number-based series of files, take screenshots, and interact with the mouse pointer.

    Attributes:
        generalPath (str): The main path of the project.
        paths (dict): A dictionary containing paths of files and directories.
        directories (dict): A dictionary containing directories.

    Methods:
        __init__: Initializes the class instance.
        pathways(mainPath=None, files=True): Generates a nested structure representing directories and files in a given path.
        image(show=False): Takes a screenshot of the current screen and returns it as a PIL image.
        mouse(dataPoint): Moves the mouse pointer to a specified location of an element and then clicks it.
    """

    generalPath = ""
    color = (248, 93, 94)

    def __init__(self):
        """
        Initializes the class instance.

        Args:
            None.

        Returns:
            None.
        """
        self.generalPath = pathlib.Path(
            __file__).parent.parent.resolve().as_posix()

    def image(self):
        """
        Takes a screenshot of the current screen and returns it as a PIL image.

        Returns:
            tuple: A tuple containing first the file path and then the Pillow image.
        """
        screenshot = pyautogui.screenshot()
        return np.array(screenshot)

    def mouse(self, dataPoint, clicks):
        """
        Moves the mouse pointer to a specified location of an element and then clicks it..

        Args:
            dataPoint (list): A list containing either the (x, y) coordinates of a point or a sublist of text data in the format [left, top, right, bottom, confidence, text].

        Returns:
            None.

        Notes:
            The method uses the PyAutoGUI library to move the mouse pointer. The coordinates of the mouse pointer are scaled based on the current screen resolution.
        """
        pyautogui.moveTo(dataPoint[0], dataPoint[1])
        pyautogui.click(clicks=clicks)

class pipeline:
    """
    A class to identify and select items on the screen.

    The Identifier class processes images, extracting  information, and allows users to interact with regions of interest. It uses the libraries "pyautogui," "pytesseract," "PIL," "cv2," and "re."

    Attributes:
        image_path (str): The path to the image file.
        processed_image (PIL.Image): The processed image.
        converted_image (ndarray): The image converted to an appropriate format for processing.
        original_image (PIL.Image): The original, unprocessed image.
        data (list): The extracted data from the image.
        coordinate_data (dict): A dictionary containing the processed data with coordinates.
        selected_coordinate (tuple): The selected coordinate from the coordinate_data.
        x (system.System): An instance of the System class.

    Example:
        >>> identifier()
    """
    processed_image = None
    original_image = None
    contours = None
    coordinate_data = list()
    selected_coordinate = None
    x = system()
    exit_flag = False


    def __init__(self):
        """
        The `Identifier` class' initializer.

        Args:
            x (object, optional): An instance of the `Main` class. Defaults to None.

        Raises:
            None.
        
        Notes:
            Initializes the `Identifier` class and its methods. This initializer automatically performs the usage pipeline.
        """
    
    def run(self, clicks=1):
        self.contours = list()
        self.original_image = None
        self.processed_image = None
        self.coordinate_data = list()
        self.exit_flag = False
        self.selected_coordinate = None
        self.original_image = self.x.image()
        self.processing_image()
        self.collecting_data()
        self.processing_data()
        self.exit_flag = self.selecting_coordinate(clicks=clicks)


    def processing_image(self):
        """
        Performs image processing on an input .png image stored in a PIL Image.

        Args:
            self (object): An instance of this method's class "Identifier."

        Returns:
            None.

        Raises:
            None.

        Notes:
            The processed image is stored in the `self.processed_image` variable, and the original image is converted to RGB format and stored in the `self.original_image` variable. The `self.converted_image` variable stores a copy of the converted image as a numpy array. 
        """
        image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
        allContours = []
        for i in range(1, 8):
            thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
            kernel = np.ones((1, i), np.uint8)
            dilated = cv2.dilate(thresh, kernel, iterations=1)
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) < 525:
                allContours.append(contours)
                self.contours = max(allContours, key=len)
            if len(self.contours) > 300:
                break
        
    def collecting_data(self):
        """
        Extracts data from an image using optical character recognition.

        Args:
            self (object): An instance of this method's class "Identifier."

        Returns:
            None.

        Raises:
            None.

        Notes:
            The `self.processed_image` variable must be set to the input image. The extracted data is stored as a list of lists, where each inner list represents a region of interest following the format [left, top, right, bottom, confidence, text].
        """

        """
        The data follows the format [ 0 'level', 1 'page_num', 2 'block_num', 3 'par_num', 4 'line_num', 5 'word_num', 6 'left', 7 'top', 8 'width', 9 'height', 10 'conf', 11 'text']

        """
        for cnt in self.contours:
            x, y, w, h = cv2.boundingRect(cnt)
            self.coordinate_data.append([x, y, x + w, y + h])

    
    def processing_data(self):
        """
        Filters a list of text data chunks based on their properties into coordinate data.

        Args:
            self (object): An instance of this method's class "Identifier."

        Returns:
            None.

        Raises:
            None.

        Notes:
            The `self.data` variable must be set to a list of data chunks before calling this method. Each data point should follow the format [left, top, width, height, confidence, and extracted text]. This method filters the data points based on their bounding boxes using the intersection over union (IoU) method. The `self.data` variable is updated to contain the filtered list. The `self.coordinate_data` variable is also updated to contain a dictionary that maps each chunk's left and top coordinates to a unique alphabet string identifier.
        """
        def intersection_over_union(data_point_1, data_point_2):
            p1x1, p1y2, p1x2, p1y2 = data_point_1
            p2x1, p2y1, p2x2, p2y2 = data_point_2
            xInter1 = max(p1x1, p2x1)
            yInter1 = max(p1y2, p2y1)
            xInter2 = min(p1x1 + p1x2, p2x1 + p2x2)
            yInter2 = min(p1y2 + p1y2, p2y1 + p2y2)
            interArea = max(0, xInter2 - xInter1) * \
                max(0, yInter2 - yInter1)
            area1 = p1x2 * p1y2
            area2 = p2x2 * p2y2
            return [interArea, area1, area2]

        def remove_intersecting_boxes(data_points):
            rt = index.Index()
            for i, data_point in enumerate(data_points):
                try:
                    rt.insert(
                        i, (data_point[0], data_point[1], data_point[2], data_point[3]))
                except:
                    print((data_point[0], data_point[1], data_point[2], data_point[3]))
            boxes_to_remove = set()
            for i, data_point in enumerate(data_points):

                intersectingIndices = list(rt.intersection(
                    (data_point[0], data_point[1], data_point[2], data_point[3])))
                if len(intersectingIndices) > 1:
                    for j in intersectingIndices:
                        if i != j:
                            interArea, area1, area2 = intersection_over_union(
                                data_points[i], data_points[j])
                            if interArea > 50:
                                if area1 > area2:
                                    boxes_to_remove.add(i)
            for i in boxes_to_remove:
                rt.delete(i, (data_points[i][0],
                                data_points[i][1],
                                data_points[i][2], data_points[i][3]))
            allItems = list()
            for item in rt.intersection((float('-inf'), float('-inf'), float('inf'), float('inf'))):
                allItems.append(data_points[item])
            return allItems
        
        self.coordinate_data = remove_intersecting_boxes(self.coordinate_data)

        
        def generate_alphabet_strings(length, current_string="", alphabet="etaoinsrhlcdumfpwybgvkxjq"):
            if length == 1:
                for letter in alphabet:
                    yield current_string + letter
            else:
                for letter in alphabet:
                    yield from generate_alphabet_strings(length - 1, current_string + letter, alphabet)

        def list_aphabet_strings(items):
            num_items = len(items)
            alphabet_length = 25
            string_length = 1

            while alphabet_length ** string_length < num_items:
                string_length += 1

            alphabet_strings = list(generate_alphabet_strings(string_length))[
                : num_items]

            return list(zip(alphabet_strings, items))

        toMap = [(item[0], item[1]) for item in self.coordinate_data]
        self.coordinate_data = list_aphabet_strings(toMap)


    def selecting_coordinate(self, clicks):
        """
        Allows the user to select a coordinate location from the regions of interest.

        Args:
            self (object): An instance of this method's class "Identifier."

        Returns:
            None.

        Raises:
            None.

        Notes:
            This method displays the input image on a tkinter canvas with keyboard controls enabled. The user can enter a letter to filter the displayed text chunks by their first letter. Pressing the letter corresponding to the desired text chunk's first letter selects that chunk's coordinate location as the "selected_coordinate" variable. The selected coordinate is stored as a tuple in the format (x, y).
        """
        keys = [full_input_identifier for full_input_identifier, _ in self.coordinate_data]
        length = len(keys[0])
        key_buffer = []

        def on_press(key):
            try:
                key_buffer.append(key.char.lower())
            except AttributeError:
                pass

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        def edited_image(listed_data, image, root):
            "key should be a string, location should be in the format (x, y)"
            for key, loc in listed_data:
                cv2.rectangle(image, (loc[0], loc[1]), (loc[0] + 20, loc[1] + 20), self.x.color, -1)
                text_size, _ = cv2.getTextSize(
                    key, cv2.FONT_HERSHEY_SIMPLEX, 0.48, 1)
                text_x = loc[0] + (20 - text_size[0]) // 2
                text_y = loc[1] + (20 + text_size[1]) // 2
                cv2.putText(image, key, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                            (0, 0, 0), 1, cv2.LINE_AA)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            iosuccess, buffer = cv2.imencode(".png", image)
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                temp_file.write(buffer.tobytes())
                return tk.PhotoImage(file=temp_file.name)


        def update_list(input_char, items):
            filtered_items = [
                    (input_identifier, point) for input_identifier, point in items if input_identifier[0].lower() == input_char.lower()]
            return [(k[len(input_char):], v) for k, v in filtered_items]
            
        update = self.coordinate_data.copy()
        test = "".join(key_buffer[-length:]) not in keys 
        for i in range(length):
            root = tk.Tk()
            image = self.original_image.copy()
            root.wm_attributes('-fullscreen', True)
            root.focus_force()
            python_image = edited_image(update, image, root)
            ttk.Label(root, image=python_image).pack()
            root.after(1, lambda: root.focus_force())
            root.bind("<Key>", lambda e: root.destroy())
            root.mainloop()
            try:
                update = update_list(key_buffer[-1], update)
                test = "".join(key_buffer[-length:]) not in keys
                if len(update) == 0 or len(update) == 1 or len(key_buffer) != (i+1):
                    break
            except IndexError:
                break

        listener.stop()
        try:
            self.selected_coordinate = {k: v for k, v in self.coordinate_data}["".join(key_buffer[-length:])]
            time.sleep(0.15)
            self.x.mouse([self.selected_coordinate[0]+5, self.selected_coordinate[1]+5], clicks=clicks)
            return False
        except KeyError:
            def rgb_to_hex(rgb):
                r, g, b = rgb
                return f"#{r:02x}{g:02x}{b:02x}"

            def select_color():
                color = cc.askcolor()[1]
                if color:
                    if isinstance(color, str) and color.startswith('#'):
                        color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
                    self.x.color = tuple(map(int, color))
                    label.config(text=f"Selected color: {self.x.color}")
                    label.config(foreground=rgb_to_hex(self.x.color))

            def exit_app():
                global exit_flag
                exit_flag = True
                root.destroy()
                root.quit()

            global exit_flag
            exit_flag = False
            root = tk.Tk()
            root.title("KeyFlare Preferences")
            root.geometry("300x300")
            style = ThemedStyle(root)
            style.set_theme("equilux")
            label_frame = ttk.Frame(root, padding=20)
            label_frame.pack(fill="both", expand=True)
            label_frame.config(borderwidth=2, relief="groove")
            label = ttk.Label(label_frame, text="Selected color:", font=("Arial", 14), background=rgb_to_hex(self.x.color), foreground="#000000")
            label.pack()
            select_button = ttk.Button(root, text="Select Color", command=select_color)
            select_button.pack(pady=10)
            exit_button = ttk.Button(root, text="Completely Exit KeyFlare", command=exit_app)
            exit_button.pack(pady=10)
            pass_button = ttk.Button(root, text="Continue", command=root.destroy)
            pass_button.pack(pady=10)
            root.mainloop()
            return exit_flag


def main():
    """
    Entry point for the script. Starts a keyboard listener that calls the class identifier() when the keyboard combination Shift + A + Z is pressed. An alternative method to exit the script is to press Ctrl + C on Windows or Ctrl + Z on Ubuntu.

    Args:
        None

    Returns:
        None
    """
    y = pipeline()
    start_combination = [
        {keyboard.Key.alt_l, keyboard.KeyCode(char='a'), keyboard.KeyCode(char='z')},
        {keyboard.Key.alt_r, keyboard.KeyCode(char='a'), keyboard.KeyCode(char='z')}
    ]

    current = set()
    global left_pressed, right_pressed
    left_pressed = False
    right_pressed = False

    def on_press(key):
        global y, left_pressed, right_pressed
        if key == keyboard.Key.alt_l:
            left_pressed = True
        elif key == keyboard.Key.alt_r:
            right_pressed = True
        if any([key in COMBO for COMBO in start_combination]):
            current.add(key)
            if any(all(k in current for k in COMBO) for COMBO in start_combination):
                if left_pressed:
                    y.run()
                elif right_pressed:
                    y.run(clicks=2)
                    
    def on_release(key):
        global left_pressed, right_pressed
        if key == keyboard.Key.alt_l:
            left_pressed = False
        elif key == keyboard.Key.alt_r:
            right_pressed = False
        if any([key in COMBO for COMBO in start_combination]):
            try:
                current.remove(key)
            except:
                pass
        
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while True:
        try:
            time.sleep(1)
            if y.exit_flag:
                sys.exit()
        except KeyboardInterrupt:
            break
    listener.stop()


if __name__ == "__main__":
    main()