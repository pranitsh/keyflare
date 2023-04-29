#!/usr/bin/env poetry run python3
import tkinter as tk
from pynput import keyboard
import time
import numpy as np
import pytesseract
import re
import pyautogui
import cv2
import time
from PIL import Image, ImageTk
import string
from rtree import index
import glob
import pathlib
import pyautogui
import PIL
import os
import urllib.request
from sys import exit

pytesseract.pytesseract.tesseract_cmd = r'C:\\\Program Files\\\Tesseract-OCR\\\tesseract.exe'

class system:
    """
    A class to manage files and directories, create a number-based series of files, take screenshots, and interact with the mouse pointer.

    Attributes:
        generalPath (str): The main path of the project.
        paths (dict): A dictionary containing paths of files and directories.
        directories (dict): A dictionary containing directories.
        folders (dict): A dictionary containing file extensions for different series folders.

    Methods:
        __init__: Initializes the class instance.
        pathways(mainPath=None, files=True): Generates a nested structure representing directories and files in a given path.
        series(series, new=True, file=True): Helps to manage a number-based series of files within a specified directory.
        image(show=False): Takes a screenshot of the current screen and returns it as a PIL image.
        mouse(dataPoint): Moves the mouse pointer to a specified location of an element and then clicks it.
    """

    generalPath = ""
    folders = {"logs": ".log", "learning": ".toml", "data": ".pkl", "training": ".h5", "history": ".p", "highlights": ".toml",
               "photos": ".png", "reviews": ".yaml", "docs": ".md", "tasks": ".toml", "readable": ".toml", "tests": ".py",
               "logsnext": "", "src": ".py", "screenshots": ".png"}

    def __init__(self, fast=True):
        """
        Initializes the class instance.

        Args:
            fast (bool): A boolean value indicating whether to use fast processing mode. Default is False.

        Returns:
            None.
        """
        self.generalPath = pathlib.Path(
            __file__).parent.parent.resolve().as_posix()
        if fast == False:
            self.check()
            print("[system] Initiated.")

    def check(self):
        url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
        urllib.request.urlretrieve(url, self.series("screenshots"))
        img = Image.open(self.series("screenshots", new=False)[-1])
        try:
            text = pytesseract.image_to_string(img, lang = 'eng')
            print("[system] If the following text reads google, everything has been tested:", text)
        except pytesseract.TesseractNotFoundError:
            print("[system] Unable to run pytesseract, please download tesseract at https://github.com/UB-Mannheim/tesseract/wiki")
            print("[system] Make sure to install it in the default location: C:\\Program Files\\Tesseract-OCR")
            print("[system] Exiting in 20 seconds")
            time.sleep(20)
            exit()
        
    def series(self, series, new=True, file=True):
        """
        Helps to manage a number-based series of files within a specified directory.

        Args:
            series (str): The name of the series folder.
            new (bool, optional): If True, creates a new file or folder. If False, retrieves existing file versions. Defaults to True.
            file (bool, optional): If True, creates a file. If False, creates a folder. Defaults to True.

        Returns:
            Union[str, List[str]]: If new is True, returns the full path to the newly created file or folder. If new is False, returns a list of full paths to existing files in the series.
        """
        folderPath = ""
        extension = ""
        try:
            extension = self.folders[series]
        except KeyError:
            extension = input(
                f"[system] {series} should use what extension: ")
            if "." not in extension:
                extension = "." + extension
        
        folderPath = pathlib.Path(self.generalPath, series)
        folderPath.mkdir(parents=True, exist_ok=True)
        folderPath = folderPath.as_posix()
        
        allFiles = dict()
        useDict = False
        for file in os.listdir(folderPath):
            file = str(file)
            if "." in file:
                try:
                    file = file.split(".")[0]
                    allFiles[int(file)] = folderPath + \
                        "/" + file + extension
                except ValueError:
                    useDict = True
                    file = file.split(".")[0]
                    allFiles[file] = folderPath + \
                        "/" + file + extension
        allFiles = list(allFiles.values())
        allFiles.sort(key=os.path.getmtime)
        if new == False:
            if len(allFiles) == 0:
                fileName = "0" + extension
                fullPath = f"{folderPath}/{fileName}"
                pathlib.Path(fullPath).touch()
                allFiles.append(fullPath)
            return allFiles
        elif new == True:
            fileName = str(len(allFiles)) + extension
            fullPath = f"{folderPath}/{fileName}"
            if file:
                pathlib.Path(fullPath).touch()
            elif file == False:
                pathlib.Path(fullPath).mkdir()
            return fullPath
    
    def image(self, show=False):
        """
        Takes a screenshot of the current screen and returns it as a PIL image.

        Args:
            show (str, optional): If specified, opens the image at the specified file path instead of taking a screenshot. Defaults to False.

        Returns:
            tuple: A tuple containing first the file path and then the Pillow image.

        Notes:
            To use pyautogui on Linux, run ```sudo apt-get install scrot```.
        """
        if show == False:
            image_path = self.series("screenshots", new=True)
            screenshot = pyautogui.screenshot()
            screenshot.save(image_path)
            return (image_path, PIL.Image.open(image_path))
        if show != False:
            im = PIL.Image.open(show)
            im.show()

    def mouse(self, dataPoint):
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
        pyautogui.click()

class identifier:
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
    image_path = None
    processed_image = None
    converted_image = None
    original_image = None
    collecting_data = list()
    coordinate_data = dict()
    selected_coordinate = None
    x = system()

    def __init__(self, x=None):
        """
        The `Identifier` class' initializer.

        Args:
            x (object, optional): An instance of the `Main` class. Defaults to None.

        Raises:
            None.
        
        Notes:
            Initializes the `Identifier` class and its methods. This initializer automatically performs the usage pipeline.
        """
        if x != None:
            self.x = x
        self.image_path, self.original_image = self.x.image()
        self.processing_image()
        self.collecting_data()
        self.processing_data()
        self.selecting_coordinate()
        if self.selected_coordinate != None:
            time.sleep(0.2)
            self.x.mouse([self.selected_coordinate[0]+5, self.selected_coordinate[1]+5])
        else:
            print("[identifier] Manually cancelled.")

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
        self.original_image = self.original_image.convert("RGB")
        cvImage = np.array(self.original_image)
        self.converted_image = cvImage[:, :, ::-1].copy()
        gray = cv2.cvtColor(self.converted_image, cv2.COLOR_RGB2GRAY)
        self.processed_image = gray
        
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
        unprocessedData = pytesseract.image_to_data(
            self.processed_image, lang='eng')
        data = []
        for thing in re.split("\n", unprocessedData):
            subList = []
            for item in re.split("\t", thing):
                try:
                    item = int(item)
                    subList.append(item)
                except ValueError:
                    subList.append(item)
            if len(subList) >= 12:
                data.append(
                    [subList[6], subList[7], subList[6]+subList[8], subList[7]+subList[9], subList[10], subList[11]])
        self.collecting_data = data[1:]

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
        items = list()
        rt = index.Index()

        def intersection_over_union(data_point_1, data_point_2):
            p1x1, p1y2, p1x2, p1y2, _, _ = data_point_1
            p2x1, p2y1, p2x2, p2y2, _, _ = data_point_2
            xInter1 = max(p1x1, p2x1)
            yInter1 = max(p1y2, p2y1)
            xInter2 = min(p1x1 + p1x2, p2x1 + p2x2)
            yInter2 = min(p1y2 + p1y2, p2y1 + p2y2)
            interArea = max(0, xInter2 - xInter1) * \
                max(0, yInter2 - yInter1)
            area1 = p1x2 * p1y2
            area2 = p2x2 * p2y2
            # union_area = area1 + area2 - inter_area
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
                            if interArea > 1:
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
            items = remove_intersecting_boxes(self.collecting_data)
            self.collecting_data = items


        def generate_alphabet_strings(length, current_string="", alphabet=string.ascii_lowercase):
            if length == 1:
                for letter in alphabet:
                    yield current_string + letter
            else:
                for letter in alphabet:
                    yield from generate_alphabet_strings(length - 1, current_string + letter, alphabet)

        def map_list_to_alphabet_strings(items):
            num_items = len(items)
            alphabet_length = len(string.ascii_lowercase)
            string_length = 1

            while alphabet_length ** string_length < num_items:
                string_length += 1

            alphabet_strings = list(generate_alphabet_strings(string_length))[
                : num_items]

            return {alphabet_string: item for alphabet_string, item in zip(alphabet_strings, items)}

        toMap = [(item[0], item[1]) for item in self.collecting_data]
        self.coordinate_data = map_list_to_alphabet_strings(toMap)


    def selecting_coordinate(self):
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
        keys = list(self.coordinate_data.keys())
        length = len(keys[0])
        key_buffer = [""]

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
                x, y, w, h = loc[0], loc[1], 20, 20
                cv2.rectangle(image, (x, y), (x + w, y + h), (248, 240, 202), -1)
                # image = cv2.addWeighted(
                #     image, alpha, self.fullImage, 1 - alpha, 0)
                text_size, _ = cv2.getTextSize(
                    key, cv2.FONT_HERSHEY_TRIPLEX, 0.45, 1)
                text_x = x + (w - text_size[0]) // 2
                text_y = y + (h + text_size[1]) // 2
                cv2.putText(image, key, (text_x, text_y), cv2.FONT_HERSHEY_TRIPLEX, 0.45,
                            (0, 0, 0), 1, cv2.LINE_AA)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image)
            tk_image = ImageTk.PhotoImage(pil_image)
            return tk_image

        def update_dict(input_char, dict_items):
            try:
                assert len(dict_items)>0
            except TypeError or AssertionError:
                exit()
            toReturn = None
            if input_char != "":
                try:
                    filtered_items = [
                        (k, v) for k, v in dict_items if k[0].lower() == input_char.lower()]
                    toReturn = [(k[1:], v) for k, v in filtered_items]
                except IndexError:
                    exit()
            else:
                if isinstance(dict_items, dict):
                    toReturn = list(dict_items.items())
            try:
                if len(toReturn):
                    return toReturn
            except TypeError:
                exit()
            else:
                return None

        update = self.coordinate_data.copy()
        while "".join(key_buffer[-length:]) not in keys:
            image = self.converted_image.copy()
            root = tk.Tk()
            root.title("Screenshot with Keyboard Controls")
            canvas = tk.Canvas(
                root, width=image.shape[1], height=image.shape[0])
            canvas.pack()
            root.wm_attributes("-topmost", True)
            image = self.converted_image.copy()
            update = update_dict(key_buffer[-1], update)
            if update == None:
                break
            root.lift()
            root.focus_force()
            height, width, left, top = image.shape[1], image.shape[0], 0, 0 
            root.geometry(f"{height}x{width}+{left}+{top}")
            root.wm_attributes('-fullscreen', 'True')
            tk_image = edited_image(update, image, root)
            canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
            root.after(1, lambda: root.focus_force())
            root.bind("<Key>", lambda e: root.destroy())
            root.mainloop()

        if "".join(key_buffer[-length:]) in keys:
            self.selected_coordinate = self.coordinate_data["".join(key_buffer[-length:])]

        listener.stop()

def main():
    identifier(x=system(fast=False))
    start_combination = [
        {keyboard.Key.shift, keyboard.KeyCode(char='a'), keyboard.KeyCode(char='z')},
        {keyboard.Key.shift, keyboard.KeyCode(char='A'), keyboard.KeyCode(char='Z')}
    ]

    current = set()

    def on_press(key):
        if any([key in COMBO for COMBO in start_combination]):
            current.add(key)
            if any(all(k in current for k in COMBO) for COMBO in start_combination):
                identifier()
            
    def on_release(key):
        if any([key in COMBO for COMBO in start_combination]):
            current.remove(key)


    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # Keep the main thread alive
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    
    listener.stop()


if __name__ == "__main__":
    main()
