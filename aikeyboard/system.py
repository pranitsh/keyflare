#!/usr/bin/env poetry run python3
import glob
import pathlib
import itertools
import pyautogui
import PIL
import os

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
    paths = dict()
    directories = dict()
    folders = {"logs": ".log", "learning": ".toml", "data": ".pkl", "training": ".h5", "history": ".p", "highlights": ".toml",
               "photos": ".png", "reviews": ".yaml", "docs": ".md", "tasks": ".toml", "readable": ".toml", "tests": ".py",
               "logsnext": "", "src": ".py", "screenshots": ".png"}

    def __init__(self):
        """
        Initializes the class instance.

        Args:
            fast (bool): A boolean value indicating whether to use fast processing mode. Default is False.

        Returns:
            None.
        """
        self.generalPath = pathlib.Path(
            __file__).parent.parent.resolve().as_posix()
        self.pathways(self.generalPath)
        print("[system] Initiated.")

    def pathways(self, mainPath=None, files=True):
        """
        Generates a nested structure representing directories and files in a given path.

        Args:
            mainPath (str, optional): The main path to process. Defaults to None.
            files (bool, optional): Determines if the method should return files. Defaults to True.

        Returns:
            Union[Dict[str, Union[str, List[str]]], Dict[str, str]]: A nested structure representing the directories and files in the given path.
        """

        if mainPath == None:
            mainPath = self.generalPath
        update = False
        if mainPath == self.generalPath:
            update = True

        mainDirectories = ""
        mainDirectories = str(mainPath)

        def allPathways(inputPath):
            inputPath = os.path.abspath(inputPath)
            if inputPath[-1] == "/":
                inputPath = inputPath[:-1]
            pathlibPath = pathlib.Path(inputPath)
            if pathlibPath.exists() and pathlibPath.is_dir():
                dictPath = dict()
                useDict = False
                for path in glob.glob(pathlibPath.absolute().as_posix() + "/*", recursive=True):
                    name = os.path.basename(path)
                    if pathlib.Path(path).is_dir():
                        useDict = True
                    if name[0] != ".":
                        dictPath[name] = allPathways(path)
                if useDict == False:
                    dictPath = list(dictPath.values())
                    dictPath.sort(key=os.path.getmtime)
                return dictPath
            elif pathlibPath.exists() and pathlibPath.is_file():
                return inputPath
            elif not pathlibPath.exists():
                print("[system] Could not interpret", inputPath)
        mainPath = allPathways(mainPath)

        def allDirectories(inputPath):
            inputPath = os.path.abspath(inputPath)
            if os.path.isfile(inputPath):
                inputPath = pathlib.Path(
                    mainPath).parent.absolute().as_posix()
            if inputPath[-1] == "/":
                inputPath = inputPath[:-1]
            pathlibPath = pathlib.Path(inputPath)
            if pathlibPath.exists() and pathlibPath.is_dir():
                dictPath = dict()
                subFolders = glob.glob(
                    pathlibPath.absolute().as_posix() + "/*/", recursive=True)
                for path in subFolders:
                    path = path[:-1]
                    name = os.path.basename(path)
                    dictPath[name] = path
                return dictPath
        mainDirectories = allDirectories(mainDirectories)
        if update:
            self.paths = mainPath
            self.directories = mainDirectories
        if files:
            return mainPath
        elif files == False:
            return mainDirectories

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
        try:
            folderPath = self.directories[series]
        except KeyError:
            folderPath = self.generalPath + "/" + series
            print('[system] Creating series folder')
            os.mkdir(folderPath)
            self.directories[series] = folderPath
        allFiles = dict()
        useDict = False
        for file in os.listdir(folderPath):
            file = str(file)
            if "." in file:
                try:
                    file = file.split(".")[0]
                    allFiles[int(file)] = self.directories[series] + \
                        "/" + file + extension
                except ValueError:
                    useDict = True
                    file = file.split(".")[0]
                    allFiles[file] = self.directories[series] + \
                        "/" + file + extension
        allFiles = list(allFiles.values())
        allFiles.sort(key=os.path.getmtime)
        if new == False:
            if len(allFiles) == 0:
                fileName = "0" + extension
                fullPath = f"{folderPath}/{fileName}"
                print(fullPath)
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
            print(image_path, screenshot.size)
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
        print("[system] Moving mouse to", dataPoint)
        pyautogui.moveTo(dataPoint[0], dataPoint[1])
        pyautogui.click()