#!/usr/bin/env poetry run python3
# from scamp import *
import os
import glob
import datetime
import logging
import subprocess
import pathlib
import pyperclip
import itertools
import re
import sqlite3
import json
import filecmp
import math
import asyncio
import shelve
import random
import pyautogui
import PIL


class System:
    generalPath = ""
    paths = dict()
    directories = dict()
    folders = {"logs": ".log", "learning": ".toml", "data": ".pkl", "training": ".h5", "history": ".p", "highlights": ".toml",
               "photos": ".png", "reviews": ".yaml", "docs": ".md", "tasks": ".toml", "readable": ".toml", "tests": ".py",
               "logsnext": "", "src": ".py", "screenshots": ".png"}

    def __init__(self, toCreate, fast=False, createFolders=False, project_folder=None, removeFolders=False):
        self.generalPath = pathlib.Path(
            __file__).parent.parent.resolve().as_posix()
        if project_folder != None:
            self.generalPath = project_folder
        self.pathways(self.generalPath)
        self.cleaning()
        self.createFiles(fast)
        print("[System] Initiated and passed testing")

    def pathways(self, mainPath=None, files=True):
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
                print("[System] Could not interpret", inputPath)
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
        """Features
           + Create a new file if new==True, or get versions with new==False
           + Create a series folder with a different file extension attached to a database
           + Asks for file extension if it does not exist yet
           Issues
           - Disregards subfolders in folders
           - Full safeties not built-in
        """
        folderPath = ""
        extension = ""
        try:
            extension = self.folders[series]
        except KeyError:
            extension = input(
                f"[System] {series} should use what extension: ")
            if "." not in extension:
                extension = "." + extension
        try:
            folderPath = self.directories[series]
        except KeyError:
            folderPath = self.generalPath + "/" + series
            print('[System] Creating series folder')
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

    def createFiles(self, fast=False):
        if fast == False:
            self.database('toNotDelete')
            self.write(self.series("docs", new=False)[-1])

    def write(self, path, reading=None, listed=False):
        """
        Features:
        + Creates file if it doesn't exist
        + Get file as a list of lines or as one string
        Issues:
        - Only works with files that definitely exist
        - Only works with files that are unicode
        """
        if reading == None:
            try:
                if listed == False:
                    with open(path, 'r', encoding="utf-8") as file:
                        try:
                            text = file.read()
                        except UnicodeDecodeError:
                            return str(random.randint(0, 1000000))
                elif listed == True:
                    with open(path, 'r', encoding="utf-8") as file:
                        text = file.readlines()
                return text
            except FileNotFoundError:
                return ""
        elif reading != None:
            with open(path, 'w', encoding="utf-8") as file:
                file.write(reading)
            return self.write(path=path)

   
    def cleaning(self):
        """Cleaning up the files
        Features:
        + Removes empty files
        Issues:
        - Does not delete duplicates.
        - Should be improved so that all files are created and tested and that this removes files not meant to be initialized.
        - Shouldn't delete the newest file
        """
        allFiles = []
        for name in list(self.directories.keys()):
            fileOptions = glob.glob(
                self.directories[name] + "/*/")
            for each in fileOptions:
                each = each[:-1]
                if os.path.isfile(each):
                    allFiles += each
        toNotDelete = self.database("toNotDelete")
        for fileA, fileB in itertools.combinations(allFiles, 2):
            content1 = self.write(path=fileA)
            content2 = self.write(path=fileB)
            path1 = pathlib.Path(fileA)
            size1 = path1.stat().st_size
            path2 = pathlib.Path(fileB)
            size2 = path2.stat().st_size
            if content1 == content2:
                last_modified1 = path1.stat().st_mtime
                last_modified2 = path2.stat().st_mtime
                if last_modified1 >= last_modified2:
                    ifRemoving = input(
                        f"[System] Planning to remove {str(path1)}, Y/n: ") == "Y"
                    if str(path2) not in toNotDelete:
                        if ifRemoving:
                            os.remove(path1)
                            allFiles.remove(path1)
                        elif not ifRemoving:
                            self.database(
                                "toNotDelete", data=path1.as_posix())
                elif last_modified1 < last_modified2:
                    if str(path2) not in toNotDelete:
                        if ifRemoving:
                            os.remove(path2)
                            allFiles.remove(path2)
                        elif not ifRemoving:
                            self.database(
                                "toNotDelete", data=path2.as_posix())
        for each in allFiles:
            if os.path.getsize(each) < 10:
                ifRemoving = input(
                    f"[System] Too small, remove? {str(each)} Y/n: ") == "Y"
                if str(each) not in toNotDelete:
                    if ifRemoving:
                        os.remove(each)
                        allFiles.remove(each)
                    elif not ifRemoving:
                        self.database("toNotDelete", data=str(each))

    def database(self, category, data=None, remove=False):
        """
        Features
        + Persistent database
        + Fast for small databases
        + Allows dictionaries
        Issues
        - No cleaning
        - Only works with small databases
        """
        if data != {} and data != [] and data != "":
            with shelve.open(self.generalPath + "/data.db", writeback=True) as db:
                try:
                    check = list(db[category])
                except:
                    db[category] = list()
                    check = list()
                    print(f"[System] [Database] Created category {category}")
                if remove == True:
                    check.remove(data)
                    print(f"[System] [Database] {category} Removing data")
                    db[category] = check
                    return check
                if isinstance(check, list):
                    if data not in check and data != None:
                        if len(data) != 0:
                            if isinstance(data, str) and data.strip() != "":
                                if remove == False:
                                    check.append(data)
                                db[category] = check
                            else:
                                if remove == False:
                                    check.append(data)
                                db[category] = check
                        else:
                            print(
                                f"[System] [Database] {category} Data is empty")
                    elif data in check:
                        print(
                            f"[System] [Database] {category} Data already saved")
                    elif data == None:
                        return list(check)
        else:
            print(f"[System] [Database] {category} Data is empty")

    
    def image(self, show=False):
        """Takes an image and returns it as a pillow image. This does not capture the mouse."""
        if show == False:
            imagePath = self.series("screenshots", new=True)
            # To use pyautogui on linux, run ```sudo apt-get install scrot```
            myScreenshot = pyautogui.screenshot()
            print(imagePath)
            myScreenshot.save(imagePath)
            return (imagePath, PIL.Image.open(imagePath))
        if show != False:
            im = PIL.Image.open(show)
            im.show()

    def mouse(self, dataPoint, returnLocation=False, printing=False):
        """The "identifyingLocations(self, chunks)" method takes a list of "chunks," representing extracted text data and its properties, and calculates the central location of each text element based on its bounding box coordinates and dimensions."""
        if len(dataPoint) == 2:
            if printing == True:
                print("[System] Moving mouse to", dataPoint)
            pyautogui.moveTo(dataPoint[0], dataPoint[1])
            pyautogui.click()
            if returnLocation == True:
                return dataPoint
        else:
            boundingBox = [dataPoint[6], dataPoint[7], dataPoint[6] +
                           dataPoint[8], dataPoint[7]+dataPoint[9]]
            location = [boundingBox[0] + boundingBox[2]/2,
                        boundingBox[1] + boundingBox[3]/2]
            location = [location[0] * 0.6725, location[1] * 0.6725]
            if printing == True:
                print("[System] Moving mouse to", location)
            pyautogui.moveTo(location[0], location[1])
            if returnLocation == True:
                return location
            elif returnLocation == False:
                return boundingBox
