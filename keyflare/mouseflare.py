#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import tkinter.colorchooser as cc
import numpy as np
import pyautogui
import time
import cv2
from rtree import index
import pathlib
import sys
import tempfile
import copy
import platform

class System:
    generalPath = ""

    def __init__(self):
        self.generalPath = pathlib.Path(
            __file__).parent.parent.resolve().as_posix()

    def image(self):
        screenshot = pyautogui.screenshot()
        return np.array(screenshot)

    def mouse(self, dataPoint, clicks):
        pyautogui.moveTo(dataPoint[0], dataPoint[1])
        pyautogui.click(clicks=clicks)

class ImagePipeline:
    processed_image = None
    original_image = None
    processed_contours = list()
    original_contours = list()
    coordinate_data = list()
    x = System()
    
    def run(self):
        self.coordinate_data = list()
        self.processed_contours = list()
        self.processed_image = None
        self.original_contours = list()
        self.original_image = self.x.image()
        self.processing_image()
        self.processing_data()

    def processing_image(self):
        image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
        thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        self.original_contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        kernel = np.ones((1, 4), np.uint8)
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        self.processed_contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in self.processed_contours:
            x, y, w, h = cv2.boundingRect(cnt)
            self.coordinate_data.append([x, y, w, h])
        for cnt in self.original_contours:
            x, y, w, h = cv2.boundingRect(cnt)
            self.coordinate_data.append([x, y, w, h])

    def processing_data(self):
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
                            if (self.coordinate_data[i][2]*self.coordinate_data[i][3]) <= self.coordinate_data[j][2]*self.coordinate_data[j][3]:
                                boxes_to_remove.add(j)
        for i in boxes_to_remove:
            rt.delete(i, (self.coordinate_data[i][0], self.coordinate_data[i][1], self.coordinate_data[i][0] + self.coordinate_data[i][2], self.coordinate_data[i][1]+self.coordinate_data[i][3]))
        allItems = list()
        for item in rt.intersection((float('-inf'), float('-inf'), float('inf'), float('inf'))):
            allItems.append(self.coordinate_data[item])
        self.coordinate_data = allItems

        def generate_alphabet_strings(length, current_string="", alphabet="etaoinsrhlcdumfpwybgvkxjqz"):
            if length == 1:
                for letter in alphabet:
                    yield current_string + letter
            else:
                for letter in alphabet:
                    yield from generate_alphabet_strings(length - 1, current_string + letter, alphabet)

        def list_aphabet_strings(items):
            num_items = len(items)
            alphabet_length = 26
            string_length = 1

            while alphabet_length ** string_length <= num_items:
                string_length += 1

            alphabet_strings = list(generate_alphabet_strings(string_length))[:num_items]

            return list(zip(alphabet_strings, items))

        toMap = [[item[0], item[1]] for item in self.coordinate_data]
        self.coordinate_data = list_aphabet_strings(toMap)

class GUI:
    coordinate_data = list()
    root = None
    input_char = ""
    original_image = None
    y = ImagePipeline()
    x = None
    exit_flag = False
    color = (248, 93, 94)
    label = None

    def run(self, clicks):
        self.y.run()
        self.x  = self.y.x
        self.root = tk.Tk()
        self.coordinate_data = copy.deepcopy(self.y.coordinate_data)
        self.root.title("KeyFlare")
        self.root.wm_attributes('-fullscreen', True)
        self.root.focus_force()
        self.original_image = self.y.original_image
        self.label = None
        self.selecting_coordinate(clicks)

    def selecting_coordinate(self, clicks):
        for i in range(6):
            image = self.original_image.copy()
            if self.label:
                self.label.destroy()
            if self.root.winfo_exists():
                for key, loc in self.coordinate_data:
                    image = cv2.rectangle(image, (loc[0], loc[1]), (loc[0] + 13 * len(self.coordinate_data[0][0]), loc[1] + 20), self.color, -1)
                    text_size, _ = cv2.getTextSize(key, cv2.FONT_HERSHEY_PLAIN, 0.75, 1)
                    image = cv2.putText(image, key, (loc[0] + (10 * len(self.coordinate_data[0][0]) - text_size[0]) // 2, loc[1] + (20 + text_size[1]) // 2), \
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (0, 0, 0), 1, cv2.LINE_AA)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                _, buffer = cv2.imencode(".png", image)
                with tempfile.NamedTemporaryFile(suffix='.png') as temp_file:
                    temp_file.write(buffer.tobytes())
                    image = tk.PhotoImage(file=temp_file.name)
                self.label = ttk.Label(self.root, image=image)
                self.label.pack()
                self.root.after(1, self.root.focus_force)
                self.root.bind("<Key>", self.on_key)
                self.root.mainloop()
            if len(self.coordinate_data) == 1:
                self.root.destroy()
                self.x.mouse([self.coordinate_data[0][1][0]+10, self.coordinate_data[0][1][1]+10], clicks=clicks)
                break
            elif len(self.coordinate_data) == 0:
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
        self.input_char = event.char
        self.coordinate_data = [(key[len(self.input_char):], p1) for key, p1 in self.coordinate_data if key[0].lower() == self.input_char.lower()]
        self.root.quit()

    def exit_app(self):
        self.exit_flag = True
        self.root.destroy()

    def select_color(self):
        color = cc.askcolor()[1]
        if color:
            if isinstance(color, str) and color.startswith('#'):
                color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            self.color = tuple(map(int, color))
            self.label.config(text=f"Selected color: {self.color}", background=self.rgb_to_hex(self.color))

    def rgb_to_hex(self, rgb):
        r, g, b = rgb
        return f"#{r:02x}{g:02x}{b:02x}"


def mouse_main():
    global z
    z = GUI()
    from pynput import mouse
    button_state = {'left': False, 'right': False}
    def on_click(x, y, button, pressed, button_state):
        if button == mouse.Button.left:
            button_state['left'] = pressed
        elif button == mouse.Button.right:
            button_state['right'] = pressed

        if button_state['left'] and button_state['right']:
            button_state['left'] = False
            button_state['right'] = False
            z.run(clicks=1)

    listener =  mouse.Listener(on_click=lambda x, y, button, pressed: on_click(x, y, button, pressed, button_state))
    listener.start()

    while not z.exit_flag:
        time.sleep(0.5)
    listener.stop()

def main():
    mouse_main()



if __name__ == "__main__":
    main()