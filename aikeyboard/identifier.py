#!/usr/bin/env poetry run python3
import tkinter as tk
from pynput import keyboard
import system
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

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


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
    x = system.System()

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
        print(self.processed_image.shape)    
        
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
                    key, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
                text_x = x + (w - text_size[0]) // 2
                text_y = y + (h + text_size[1]) // 2
                cv2.putText(image, key, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                            (0, 0, 0), 1, cv2.LINE_AA)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image)
            tk_image = ImageTk.PhotoImage(pil_image)
            return tk_image

        def update_dict(input_char, dict_items):
            toReturn = None
            print(input_char, len(dict_items), type(dict_items))
            if input_char != "":
                filtered_items = [
                    (k, v) for k, v in dict_items if k[0].lower() == input_char.lower()]
                toReturn = [(k[1:], v) for k, v in filtered_items]
            else:
                toReturn = list(dict_items.items())
            if len(toReturn):
                return toReturn
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
            tk_image = edited_image(update, image, root)
            canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
            root.bind("<Key>", lambda e: root.destroy())
            root.mainloop()

        if "".join(key_buffer[-length:]) in keys:
            self.selected_coordinate = self.coordinate_data["".join(key_buffer[-length:])]

        listener.stop()

def main():
    def on_press(key):
        nonlocal ctrl_pressed, shift_pressed

        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            ctrl_pressed = True
            print(ctrl_pressed)
        elif key == keyboard.Key.shift:
            shift_pressed = True
            print(shift_pressed)
        elif key == keyboard.KeyCode.from_char('Z') and ctrl_pressed and shift_pressed:
            print("i am here")
            identifier()

    def on_release(key):
        nonlocal ctrl_pressed, shift_pressed

        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            ctrl_pressed = False
            print("I was closed")
        elif key == keyboard.Key.shift:
            print("Mec")
            shift_pressed = False

    ctrl_pressed = False
    shift_pressed = False

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # Keep the main thread alive
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
