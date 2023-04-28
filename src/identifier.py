#!/usr/bin/env poetry run python3
import tkinter as tk
from pynput import keyboard
import threading
from datetime import datetime
import system
import numpy as np
import pytesseract
import re
import pyautogui
import cv2
import copy
import time
import logging
import PIL
from PIL import ImageTk
import string
from rtree import index

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


class Identifier:
    """This class will identify and classify items on the screen."""
    imagePath = None
    cvImage = None
    fullImage = None
    pilImage = None
    chunks = list()
    mappedData = dict()
    chosenItem = None
    x = system.System(False, fast=False)

    def __init__(self, x=None):
        if x != None:
            self.x = x
        self.imagePath, self.pilImage = self.x.image()
        self.processing(self.cvImage)
        self.data()
        self.processingData()
        self.mappingData()
        self.choose()
        self.x.mouse([self.chosenItem[0]+5, self.chosenItem[1]+5])
        # self.imageClassification(boundingBox=self.x.mouse(chosenItem))

    def processing(self, image, method=1):
        """The processingImage(self, image) method takes a single argument, image, which is expected to be a list with the image file path as its first element."""
        cvImage = self.pilImage.convert("RGB")
        cvImage = np.array(cvImage)
        cvImage = cvImage[:, :, ::-1].copy()
        self.fullImage = cvImage
        if method == 0:
            gray = cv2.cvtColor(cvImage, cv2.COLOR_RGB2GRAY)
            thresh = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
            equ = cv2.equalizeHist(gray)
            self.cvImage = equ
        if method == 1:
            gray = cv2.cvtColor(cvImage, cv2.COLOR_RGB2GRAY)
            self.cvImage = gray
        return self.cvImage

    def similar(self, imagePath1, imagePath2):
        """The similar(self, imagePath1, imagePath2) method takes two arguments, two absolute paths to .png images."""
        image1 = PIL.Image.open(imagePath1).convert('RGB')
        image2 = PIL.Image.open(imagePath2).convert('RGB')
        diff = PIL.ImageChops.difference(image1, image2)
        return bool(diff.getbbox())

    def data(self, method=0):
        """
        The data follows the format [ 0 'level', 1 'page_num', 2 'block_num', 3 'par_num', 4 'line_num', 5 'word_num', 6 'left', 7 'top', 8 'width', 9 'height', 10 'conf', 11 'text']

        """
        if method == 0:
            unprocessedData = pytesseract.image_to_data(
                self.cvImage, lang='eng')
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
            data = data[1:]
            self.chunks = data
        elif method == 1:
            data = list()
            edges = cv2.Canny(equ, 100, 200)
            npEdges = np.asarray(edges, dtype=bool)
            xPlus = 0
            yPlus = 0

            def findLines(arr, xPlus, yPlus):
                height, width = arr.shape[:2]
                xAxisCounts = np.sum(arr, axis=0)
                yAxisCounts = np.sum(arr, axis=1)
                # for each in np.split(xAxisCounts, 3):
                xLines = ((xAxisCounts/(height*0.45))-1)
                yLines = ((yAxisCounts/(width*0.45))-1)
                xVal, xMax = (np.argmax(xLines), np.max(xLines))
                yVal, yMax = (np.argmax(yLines), np.max(yLines))
                print()
                if xMax > yMax:
                    return [[xVal+xPlus, yPlus], [xVal+xPlus, height], arr[0:, xVal+1:], xPlus+xVal+1, yPlus]
                else:
                    return [[xPlus, yVal+yPlus], [width, yVal+1], arr[yVal+1:, 0:], xPlus, yPlus+yVal+1]
            equ = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
            for i in range(100):
                p1, p2, npEdges, xPlus, yPlus = findLines(
                    npEdges, xPlus, yPlus)
                print(p1, p2, npEdges.shape, xPlus, yPlus)
                data.append([p1, p2])
                cvImage = cv2.rectangle(
                    equ, p1, p2, (0, 255, 0), 2)
                cvImage = cv2.resize(cvImage, (0, 0), fx=0.75, fy=0.75)
                cv2.imshow("screenshot", cvImage)
                cv2.waitKey(0)
            self.chunks = data

    def viewData(self, chunks):
        """The "viewData(self, chunks)" method takes a list of "chunks," representing extracted text data and its properties. The method iterates through the "chunks" and, for each element, prints relevant information such as level, word number, confidence, and text. It then draws a rectangle around the corresponding text element on the image using the "cv2.rectangle()" function. The image is resized and displayed using "cv2.imshow()" and "cv2.waitKey(0)."""
        for each in chunks:
            # print(each)
            if type(self.cvImage) != np.ndarray:
                self.cvImage = self.processing(self.cvImage)
            cvImage = cv2.rectangle(
                self.cvImage, (each[0], each[1]), (each[2], each[3]), (0, 255, 0), 2)
            cvImage = cv2.resize(cvImage, (0, 0), fx=0.75, fy=0.75)
            cv2.imshow("screenshot", cvImage)
            cv2.waitKey(0)

    def mappingData(self):
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

        toMap = [(item[0], item[1]) for item in self.chunks]
        self.mappedData = map_list_to_alphabet_strings(toMap)

    def processingData(self, method=3):
        """The "processingData(self, chunks)" method takes a list of "chunks," representing extracted text data and its properties, and filters the elements. The method returns a list containing both groups as sublists."""
        if method == 0:
            lowConfidenceItems = []
            highConfidenceItems = []
            for each in items:
                if each[10] < 1:
                    lowConfidenceItems.append(each)
                elif each[10] >= 1:
                    highConfidenceItems.append(each)
            return (lowConfidenceItems, highConfidenceItems)
        elif method == 1:
            icons = []
            texts = []
            total = len(items)
            for num, each in enumerate(items):
                boundingBox = self.x.mouse(each)
                answer = self.imageClassification(
                    boundingBox=boundingBox, text="Is this a piece of text?")
                success = "Completed at"
                if answer == "yes":
                    texts.append(each)
                elif answer == "no":
                    icons.append(each)
                else:
                    success = "Failed at"
                print("[Identifier] [Processing]", success,
                      num, "/", total, "=", num/total)
            return (icons, texts)
        elif method == 2:
            hoverBased = []
            notHoverBased = []
            total = len(items)
            for num, each in enumerate(items):
                boundingBox = self.x.mouse(each)
                time.sleep(1)
                imagePath1 = self.imagePath
                imagePath2, _ = self.x.image()
                print("[Identifier] [Processing] Comparing",
                      imagePath1, imagePath2)
                result = self.similar(imagePath1, imagePath2)
                if result:
                    hoverBased.append(each)
                elif not result:
                    notHoverBased.append(each)
                print("[Identifier] [Processing]", "Found",
                      num, "/", total, "as", result)
            return (notHoverBased, hoverBased)
        elif method == 3:
            items = list()
            rt = index.Index()

            def intersectionOverUnion(chunk1, chunk2):
                p1x1, p1y2, p1x2, p1y2, _, _ = chunk1
                p2x1, p2y1, p2x2, p2y2, _, _ = chunk2
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

            def removeIntersectingBoxes(chunks):
                rt = index.Index()
                for i, chunk in enumerate(chunks):
                    try:
                        rt.insert(
                            i, (chunk[0], chunk[1], chunk[2], chunk[3]))
                    except:
                        print((chunk[0], chunk[1], chunk[2], chunk[3]))
                boxesToRemove = set()
                for i, chunk in enumerate(chunks):

                    intersectingIndices = list(rt.intersection(
                        (chunk[0], chunk[1], chunk[2], chunk[3])))
                    if len(intersectingIndices) > 1:
                        for j in intersectingIndices:
                            if i != j:
                                interArea, area1, area2 = intersectionOverUnion(
                                    chunks[i], chunks[j])
                                if interArea > 1:
                                    if area1 > area2:
                                        boxesToRemove.add(i)
                for i in boxesToRemove:
                    rt.delete(i, (chunks[i][0],
                                  chunks[i][1],
                                  chunks[i][2], chunks[i][3]))
                allItems = list()
                for item in rt.intersection((float('-inf'), float('-inf'), float('inf'), float('inf'))):
                    allItems.append(chunks[item])
                return allItems
            items = removeIntersectingBoxes(self.chunks)
            # filteredItems = list()
            # for each in items:
            #     if each[3]-each[1] > 1 and each[2]-each[0] > 1 and len(str(each[5])) < 15:
            #         filteredItems.append(each)
            # items = filteredItems
            print("Total Number of Items Removed in data chunks",
                  len(self.chunks)-len(items))
            print("Total Number of Items in data chunks",
                  len(items))
            self.chunks = items

    def choose(self, method=3):
        """The "chooseManually(self, locations)" method takes a list of "locations," which contains sublists of text data and their corresponding central locations in the input image."""
        if method == 0:
            toPrint = "Choose where to move the mouse from the list below\n"
            for i, item in enumerate(self.mappedData):
                print(item)
                toPrint = toPrint + str(i) + ". " + str(item[-1]) + "\n"
            print(toPrint)
            userChoice = input("Which number do you choose? ")
            try:
                userChoice = int(userChoice)
            except ValueError:
                print("You did not input a number.")
            return self.mappedData[userChoice]
        elif method == 1:
            inputChosen = ""

            def allWindows(mappedLocations, inputChosen):
                keys = list(mappedLocations.keys())

                def helperFunction(allKeys, inputChosen):
                    key_buffer = []
                    inputChosen = ""
                    length = len(allKeys)

                    def on_press(key):
                        try:
                            inputChosen = key_buffer.append(key.char.lower())
                            inputChosen = "".join(key_buffer[-length:])
                            print(inputChosen)
                        except AttributeError:
                            pass

                    listener = keyboard.Listener(on_press=on_press)
                    while inputChosen not in allKeys:
                        pass
                    listener.stop()
                    return inputChosen

                def oneWindow(targetString, allStrings, location):
                    "key should be a string, location should be in the format (x, y)"

                    root = tk.Tk()
                    root.title("Keyboard " + targetString)
                    root.geometry(f"+{location[0]}+{location[1]}")
                    root.attributes("-topmost", True)
                    root.overrideredirect(1)
                    text_elem = tk.Label(root, text=targetString, bg='white')
                    text_elem.pack()

                    key_buffer = []
                    target_sequence = list(targetString.lower())

                    def on_press(key):
                        try:
                            if key.char == target_sequence[0]:
                                text_elem.config(fg='red')
                            key_buffer.append(key.char.lower())
                            if key_buffer[-len(target_sequence):] == target_sequence:
                                root.destroy()
                            if "".join(key_buffer[-len(target_sequence):]) in allStrings:
                                root.destroy()
                        except AttributeError:
                            pass

                    listener = keyboard.Listener(on_press=on_press)
                    listener.start()

                    root.mainloop()

                    listener.stop()

                helperThread = threading.Thread(
                    target=helperFunction, args=(keys, inputChosen))
                helperThread.start()
                threads = [helperThread]
                for threadString, threadLocation in list(mappedLocations.items()):
                    print("threadString", threadString,
                          "threadLocation", threadLocation)
                    thread = threading.Thread(
                        target=oneWindow, args=(threadString, keys, threadLocation))
                    thread.start()
                    threads.append(thread)

                for thread in threads:
                    thread.join()
                return inputChosen

            inputChosen = allWindows(self.mappedData, inputChosen)
            inputChosen = self.mappedData[inputChosen]
            self.chosenItem = inputChosen
            print(self.chosenItem)
        elif method == 2:
            keys = list(self.mappedData.keys())
            length = len(keys[0])
            key_buffer = [""]

            def on_press(key):
                try:
                    key_buffer.append(key.char.lower())
                except AttributeError:
                    pass

            listener = keyboard.Listener(on_press=on_press)
            listener.start()

            def editedImage(listedData, image):
                "key should be a string, location should be in the format (x, y)"
                for key, loc in listedData:
                    x, y, w, h = loc[0], loc[1], 20, 20
                    color = (0, 0, 255)
                    alpha = 0.3

                    cv2.rectangle(image, (x, y), (x + w, y + h), color, -1)
                    # image = cv2.addWeighted(
                    #     image, alpha, self.fullImage, 1 - alpha, 0)

                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.5
                    font_thickness = 1
                    text_size, _ = cv2.getTextSize(
                        key, font, font_scale, font_thickness)
                    text_x = x + (w - text_size[0]) // 2
                    text_y = y + (h + text_size[1]) // 2
                    cv2.putText(image, key, (text_x, text_y), font, font_scale,
                                (255, 255, 255), font_thickness, cv2.LINE_AA)

                cv2.namedWindow('image', flags=cv2.WINDOW_GUI_NORMAL)
                cv2.imshow("Screenshot with Keyboard Controls", image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            def update_dict(input_char, dict_items):
                if input_char != "":
                    filtered_items = [
                        (k, v) for k, v in dict_items if k[0].lower() == input_char.lower()]
                    updated_items = [(k[1:], v) for k, v in filtered_items]
                    return updated_items
                else:
                    return list(dict_items.items())

            update = self.mappedData.copy()
            while "".join(key_buffer[-length:]) not in keys:
                image = self.fullImage.copy()
                update = update_dict(key_buffer[-1], update)
                editedImage(update, image)

            inputChosen = self.mappedData["".join(key_buffer[-length:])]
            self.chosenItem = inputChosen
            listener.stop()
            print(self.chosenItem)
        elif method == 3:
            keys = list(self.mappedData.keys())
            length = len(keys[0])
            key_buffer = [""]

            def on_press(key):
                try:
                    key_buffer.append(key.char.lower())
                except AttributeError:
                    pass

            listener = keyboard.Listener(on_press=on_press)
            listener.start()

            def editedImage(listedData, image, root):
                "key should be a string, location should be in the format (x, y)"
                for key, loc in listedData:
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
                pil_image = PIL.Image.fromarray(image)
                tk_image = ImageTk.PhotoImage(pil_image)
                return tk_image

            def update_dict(input_char, dict_items):
                toReturn = None
                if input_char != "":
                    filtered_items = [
                        (k, v) for k, v in dict_items if k[0].lower() == input_char.lower()]
                    toReturn = [(k[1:], v) for k, v in filtered_items]
                else:
                    toReturn = list(dict_items.items())
                if len(toReturn):
                    return toReturn
                else:
                    exit()

            update = self.mappedData.copy()
            while "".join(key_buffer[-length:]) not in keys:
                image = self.fullImage.copy()
                root = tk.Tk()
                root.title("Screenshot with Keyboard Controls")
                canvas = tk.Canvas(
                    root, width=image.shape[1], height=image.shape[0])
                canvas.pack()
                root.wm_attributes("-topmost", True)
                image = self.fullImage.copy()
                update = update_dict(key_buffer[-1], update)
                tk_image = editedImage(update, image, root)
                canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
                root.bind("<Key>", lambda e: root.destroy())
                root.mainloop()

            inputChosen = self.mappedData["".join(key_buffer[-length:])]
            self.chosenItem = inputChosen
            listener.stop()
            print(self.chosenItem)

    def imageClassification(self, boundingBox=None, options=1, text=None):
        if type(self.cvImage) == np.ndarray:
            self.cvImage = PIL.Image.open(self.imagePath)
            if boundingBox != None:
                image = self.cvImage.crop(boundingBox)
            else:
                image = self.cvImage
        else:
            if boundingBox != None:
                image = self.cvImage.crop(boundingBox)
            else:
                image = self.cvImage
        toReturn = "Failed"
        logger = logging.getLogger('my-logger')
        logger.setLevel(logging.ERROR)
        if options == 0:
            if self.y == None:
                from transformers import pipeline
                self.y = pipeline(
                    model="chromefan/vit-base-game-icons")
            toReturn = self.y(image)
        elif options == 1:
            if text == None:
                text = "Is this an icon?"
            if self.y == None:
                from transformers import ViltProcessor, ViltForQuestionAnswering
                processor = ViltProcessor.from_pretrained(
                    "dandelin/vilt-b32-finetuned-vqa")
                model = ViltForQuestionAnswering.from_pretrained(
                    "dandelin/vilt-b32-finetuned-vqa")
                self.y = [processor, model]
            try:
                encoding = self.y[0](image, text, return_tensors="pt")
                outputs = self.y[1](**encoding)
                logits = outputs.logits
                idx = logits.argmax(-1).item()
                toReturn = self.y[1].config.id2label[idx]
            except:
                pass
        print("[Identifier] Classified image", self.imagePath,
              "as", toReturn, "with option", "options")
        return toReturn


def main():
    Identifier()


if __name__ == "__main__":
    main()
