"""Stores the ImagePipeline class for processing the image."""
import string
import re
import numpy as np
import cv2
from rtree import index
import pytesseract
from .system import System


class ImagePipeline:
    """
    The `ImagePipeline` class performs a series of image
    processing tasks on a screenshot captured by the `System` class.
    It extracts coordinates of possibly clickable areas, removes overlapping bounding boxes,
    and labels the remaining boxes alphabetically.
    The processed data can then be used for various purposes,
    such as creating a graphical user interface (GUI) for navigating with your computer!

    Attributes:
        original_image (None):
            A placeholder for the original screenshot image.
        coordinate_data (list): A list to store coordinate data,
            including bounding boxes of clickable areas.
        x (System): An instance of the `System` class used for capturing screenshots.

    Methods:
        - run(): Executes the image processing pipeline.
        - processing_image(): Extracts contours from the
            original image into the coordinate_data.
        - processing_data(): Processes coordinate data to
            remove overlapping boxes and label the remaining boxes, recycling coordinate_data.

    Notes:
        - The `ImagePipeline` class relies on
            the `System` class for capturing the original screenshot.
        - The processed results can be accessed using the `coordinate_data` attribute.

    Example:
        >>> pipeline = ImagePipeline()
        >>> pipeline.run()  # Executes the image processing pipeline
        >>> coordinate_data = pipeline.coordinate_data
        >>> print(len(coordinate_data))  # Output: Number of labeled bounding boxes
    """

    original_image = None
    coordinate_data = []
    x = System()

    def __init__(self):
        """Defines some variables to be used later"""
        self.coordinate_data = []
        self.original_image = None
        self.converted_image = None
        self.processed_image = None
        self.collecting_data = None


    def run(self):
        """
        Executes the image processing pipeline. This method
        starts the image processing pipeline after taking a screenshot.
        The results are stored in the class as an attribute,
        which is then displayed through the GUI class.

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
        self.coordinate_data = []
        self.original_image = self.x.image()
        self.processing_image()
        self.processing_data()

    def processing_image(self):
        """
        Processes the original image to extract contours into
        coordinate data. After converting an image from grey to
        black and white with adapative thresholding, the use of
        morpohological operations expands bright spots and contracts
        dark spots. The results, the contours of the image with
        and without morphological operations,
        are stored combined for further processing.

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
        threshold = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )
        original_contours, _ = cv2.findContours(
            threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        kernel = np.ones((1, 4), np.uint8)
        dilated = cv2.dilate(threshold, kernel, iterations=1)
        processed_contours, _ = cv2.findContours(
            dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        for cnt in processed_contours:
            x, y, w, h = cv2.boundingRect(cnt)
            self.coordinate_data.append([x, y, w, h])
        for cnt in original_contours:
            x, y, w, h = cv2.boundingRect(cnt)
            self.coordinate_data.append([x, y, w, h])

    def processing_data(self):
        """
        Process the coordinate data to remove overlapping boxes and label the remaining boxes.

        This method processes the coordinate data extracted
        from the image processing step. It includes the following steps:
        1. Index the coordinate_data, which technically
           holds bounding boxes before this step,
           into the R-tree spatial indexing algorithm.
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
            >>> print(len(coordinate_data))
                # Output: Number of labeled bounding boxes

        Further Improvements:
            - Currently, if an item is overlapping another bounding box
              by 10 pixels on any side of the box, it is added to a list to be removed.
              An adaptive method designed to get a specific number of boxes would work better.
        """
        properties = index.Property()
        properties.dimension = 2
        properties.dat_extension = "data"
        properties.idx_extension = "index"
        properties.buffering_capacity = 200
        properties.pagesize = 8192
        properties.node_capacity = 100
        properties.leaf_capacity = 100
        properties.fill_factor = 0.1
        rt = index.Index(properties=properties)
        boxes_to_remove = set()
        for i, data_point in enumerate(self.coordinate_data):
            if data_point[2] * data_point[3] > 15:
                rt.insert(
                    i,
                    (
                        data_point[0],
                        data_point[1],
                        data_point[0] + data_point[2],
                        data_point[1] + data_point[3],
                    ),
                )
        for i in rt.intersection((float("-inf"), float("-inf"), float("inf"), float("inf"))):
            if i not in boxes_to_remove:
                intersectingindices = list(
                    rt.intersection(
                        (
                            self.coordinate_data[i][0] - 10,
                            self.coordinate_data[i][1] - 10,
                            self.coordinate_data[i][0]
                            + self.coordinate_data[i][2]
                            + 10,
                            self.coordinate_data[i][1]
                            + self.coordinate_data[i][3]
                            + 10,
                        )
                    )
                )
                if len(intersectingindices) > 1:
                    for j in intersectingindices:
                        if i != j:
                            if (
                                self.coordinate_data[i][2] * self.coordinate_data[i][3]
                            ) <= self.coordinate_data[j][2] * self.coordinate_data[j][
                                3
                            ] - 5:
                                boxes_to_remove.add(j)
        for i in boxes_to_remove:
            rt.delete(
                i,
                (
                    self.coordinate_data[i][0],
                    self.coordinate_data[i][1],
                    self.coordinate_data[i][0] + self.coordinate_data[i][2],
                    self.coordinate_data[i][1] + self.coordinate_data[i][3],
                ),
            )
        allitems = []
        for item in rt.intersection(
            (float("-inf"), float("-inf"), float("inf"), float("inf"))
        ):
            allitems.append(self.coordinate_data[item])
        self.coordinate_data = allitems

        def generate_alphabet_strings(
            length, current_string="", alphabet="etaoinsrhlcdumfpwybgvkxjqz"
        ):
            if length == 1:
                for letter in alphabet:
                    yield current_string + letter
            else:
                for letter in alphabet:
                    yield from generate_alphabet_strings(
                        length - 1, current_string + letter, alphabet
                    )

        def list_aphabet_strings(items):
            num_items = len(items)
            alphabet_length = 26
            string_length = 1

            while alphabet_length**string_length <= num_items:
                string_length += 1

            alphabet_strings = list(generate_alphabet_strings(string_length))[
                :num_items
            ]

            return list(zip(alphabet_strings, items))

        tomap = [[item[0], item[1], item[2], item[3]] for item in self.coordinate_data]
        self.coordinate_data = list_aphabet_strings(tomap)

    def old_run(self):
        """
        The `Identifier` class' initializer.

        Args:
            x (object, optional): An instance of the `Main` class. Defaults to None.

        Raises:
            None.

        Notes:
            Initializes the `Identifier` class and its methods.
            This initializer automatically performs the usage pipeline.
        """
        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\\\Program Files\\\Tesseract-OCR\\\tesseract.exe"
        )
        self.original_image = self.x.image()
        self.old_processing_image()
        self.old_collecting_data()
        self.old_processing_data()

    def old_processing_image(self):
        """
        Performs image processing on an input .png image stored in a PIL Image.

        Args:
            self (object): An instance of this method's class "Identifier."

        Returns:
            None.

        Raises:
            None.

        Notes:
            The processed image is stored in the `self.processed_image` variable,
            and the original image is converted to RGB format and stored in the
            `self.original_image` variable. The `self.converted_image` variable
            stores a copy of the converted image as a numpy array.
        """
        cvimage = np.array(self.original_image)
        self.converted_image = cvimage[:, :, ::-1].copy()
        gray = cv2.cvtColor(self.converted_image, cv2.COLOR_RGB2GRAY)
        self.processed_image = gray

    def old_collecting_data(self):
        """
        Extracts data from an image using optical character recognition.

        Args:
            self (object): An instance of this method's class "Identifier."

        Returns:
            None.

        Raises:
            None.

        Notes:
            The `self.processed_image` variable
            must be set to the input image. The extracted data is
            stored as a list of lists, where each inner list represents
            a region of interest following the
            format [left, top, right, bottom, confidence, text].
            The data follows the format 
                [ 0 'level', 1 'page_num', 2 'block_num', 3 'par_num', 4 'line_num',
                5 'word_num', 6 'left', 7 'top', 8 'width', 
                9 'height', 10 'conf', 11 'text']
        """
        unprocesseddata = pytesseract.image_to_data(self.processed_image, lang="eng")
        data = []
        for thing in re.split("\n", unprocesseddata):
            sublist = []
            for item in re.split("\t", thing):
                try:
                    item = int(item)
                    sublist.append(item)
                except ValueError:
                    sublist.append(item)
            if len(sublist) >= 12:
                data.append(
                    [
                        sublist[6],
                        sublist[7],
                        sublist[6] + sublist[8],
                        sublist[7] + sublist[9],
                        sublist[10],
                        sublist[11],
                    ]
                )
        self.collecting_data = data[1:]

    def old_processing_data(self):
        """
        Filters a list of text data chunks based on their properties into coordinate data.

        Args:
            self (object): An instance of this method's class "Identifier."

        Returns:
            None.

        Raises:
            None.

        Notes:
            The `self.data` variable must be set to a list of data 
            chunks before calling this method. Each data point should
            follow the format [left, top, width, height, confidence, and extracted text].
            This method filters the data points based on their bounding 
            boxes using the intersection over union (IoU) method. 
            The `self.data` variable is updated to contain the filtered list. 
            The `self.coordinate_data` variable is also updated to contain a
            dictionary that maps each chunk's left and top coordinates to a
            unique alphabet string identifier.
        """
        items = []

        def remove_intersecting_boxes(data_points):
            rt = index.Index()
            for i, data_point in enumerate(data_points):
                rt.insert(
                    i, (data_point[0], data_point[1], data_point[2], data_point[3])
                )
            boxes_to_remove = set()
            for i, data_point in enumerate(data_points):
                intersectingindices = list(
                    rt.intersection(
                        (data_point[0], data_point[1], data_point[2], data_point[3])
                    )
                )
                if len(intersectingindices) > 1:
                    for j in intersectingindices:
                        if i != j:
                            interarea, area1, area2 = self.intersection_over_union(
                                data_points[i], data_points[j]
                            )
                            if interarea > 1:
                                if area1 > area2:
                                    boxes_to_remove.add(i)
            for i in boxes_to_remove:
                rt.delete(
                    i,
                    (
                        data_points[i][0],
                        data_points[i][1],
                        data_points[i][2],
                        data_points[i][3],
                    ),
                )
            allitems = []
            for item in rt.intersection((float("-inf"), float("-inf"), float("inf"), float("inf"))):
                allitems.append(data_points[item])
            return allitems

        items = remove_intersecting_boxes(self.collecting_data)
        self.collecting_data = items

        def generate_alphabet_strings(
            length, current_string="", alphabet=string.ascii_lowercase
        ):
            if length == 1:
                for letter in alphabet:
                    yield current_string + letter
            else:
                for letter in alphabet:
                    yield from generate_alphabet_strings(
                        length - 1, current_string + letter, alphabet
                    )

        def map_list_to_alphabet_strings(items):
            num_items = len(items)
            alphabet_length = len(string.ascii_lowercase)
            string_length = 1

            while alphabet_length**string_length < num_items:
                string_length += 1

            alphabet_strings = list(generate_alphabet_strings(string_length))[
                :num_items
            ]

            return {
                alphabet_string: item
                for alphabet_string, item in zip(alphabet_strings, items)
            }

        tomap = [(item[0], item[1]) for item in self.collecting_data]
        self.coordinate_data = map_list_to_alphabet_strings(tomap)

    def intersection_over_union(self, data_point_1, data_point_2):
        """Returns the intersection over union uncalculated as a list.

        Args:
            data_point_1 (list): A list containing 6 variables for IOU.
            data_point_2 (list): A list containing 6 variables for IOU.

        Returns:
            _type_: _description_
        """
        p1x1, p1y1, width1, height1, _, _ = data_point_1
        p2x1, p2y1, width2, height2, _, _ = data_point_2
        xinter1 = max(p1x1, p2x1)
        yinter1 = max(p1y1, p2y1)
        xinter2 = min(p1x1 + width1, p2x1 + width2)
        yinter2 = min(p1y1 + height1, p2y1 + height2)
        interarea = max(0, xinter2 - xinter1) * max(0, yinter2 - yinter1)
        area1 = width1 * height1
        area2 = width2 * height2
        # union_area = area1 + area2 - inter_area
        return [interarea, area1, area2]
