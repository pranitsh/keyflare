KeyFlare
About
KeyFlare v0.1.0 is a useful tool that enables users to interactively control their mouse using their keyboard. KeyFlare can provide an expanded user experience for those who prefer to use a keyboard over a mouse.
Features:
Intuitive keyboard-based mouse control: KeyFlare shows a list of coordinates representing UI elements on your screen that you can click on by typing the unique alphabetical identifier for a coordinate of interest
Users can easily access this list of coordinates by typing shift+A+Z.
Users can conveniently exit the application by typing shift, control, or any non-shown key on the displayed image.
Users can also exit the application by deleting the terminal shown that represents the running python-based application.
Installation
For Window users:
Download the binary at KeyFlare
For linux and macOS users:
 Download python with tkinter (aka tk)
 Download poetry and add it to your path
 Download tesseract through your terminal package manager (apt for Ubuntu, brew for macOS, and so on)
 Update the keyflare/keyflare/main.py with the location of your tesseract installation (find it with which tesseract by changing this variable).
 pytesseract.pytesseract.tesseract_cmd = r'C:\\\Program Files\\\Tesseract-OCR\\\tesseract.exe
 Run it: poetry run python keyflare/main.py
I hope that KeyFlare may one day become an 
Documentation
Help on module main:

NAME
    main

CLASSES
    builtins.object
        identifier
        system

    class identifier(builtins.object)
     |  identifier(x=None)
     |
     |  A class to identify and select items on the screen.
     |
     |  The Identifier class processes images, extracting  information, and allows users to interact with regions of interest. It uses the libraries "pyautogui," "pytesseract," "PIL," "cv2," and "re."
     |
     |  Attributes:
     |      image_path (str): The path to the image file.
     |      processed_image (PIL.Image): The processed image.
     |      converted_image (ndarray): The image converted to an appropriate format for processing.
     |      original_image (PIL.Image): The original, unprocessed image.
     |      data (list): The extracted data from the image.
     |      coordinate_data (dict): A dictionary containing the processed data with coordinates.
     |      selected_coordinate (tuple): The selected coordinate from the coordinate_data.
     |      x (system.System): An instance of the System class.
     |
     |  Example:
     |      >>> identifier()
     |
     |  Methods defined here:
     |
     |  __init__(self, x=None)
     |      The `Identifier` class' initializer.
     |
     |      Args:
     |          x (object, optional): An instance of the `Main` class. Defaults to None.
     |
     |      Raises:
     |          None.
     |
     |      Notes:
     |          Initializes the `Identifier` class and its methods. This initializer automatically performs the usage pipeline.
     |
     |  collecting_data(self)
     |      Extracts data from an image using optical character recognition.
     |
     |      Args:
     |          self (object): An instance of this method's class "Identifier."
     |
     |      Returns:
     |          None.
     |
     |      Raises:
     |          None.
     |
     |      Notes:
     |          The `self.processed_image` variable must be set to the input image. The extracted data is stored as a list of lists, where each inner list represents a region of interest following the format [left, top, right, bottom, confidence, text].
     |
     |  processing_data(self)
     |      Filters a list of text data chunks based on their properties into coordinate data.
     |
     |      Args:
     |          self (object): An instance of this method's class "Identifier."
     |
     |      Returns:
     |          None.
     |
     |      Raises:
     |          None.
     |
     |      Notes:
     |          The `self.data` variable must be set to a list of data chunks before calling this method. Each data point should follow the format [left, top, width, height, confidence, and extracted text]. This method filters the data points based on their bounding boxes using the intersection over union (IoU) method. The `self.data` variable is updated to contain the filtered list. The `self.coordinate_data` variable is also updated to contain a dictionary that maps each chunk's left and top coordinates to a unique alphabet string identifier.
     |
     |  processing_image(self)
     |      Performs image processing on an input .png image stored in a PIL Image.
     |
     |      Args:
     |          self (object): An instance of this method's class "Identifier."
     |
     |      Returns:
     |          None.
     |
     |      Raises:
     |          None.
     |
     |      Notes:
     |          The processed image is stored in the `self.processed_image` variable, and the original image is converted to RGB format and stored in the `self.original_image` variable. The `self.converted_image` variable stores a copy of the converted image as a numpy array.
     |
     |  selecting_coordinate(self)
     |      Allows the user to select a coordinate location from the regions of interest.
     |
     |      Args:
     |          self (object): An instance of this method's class "Identifier."
     |
     |      Returns:
     |          None.
     |
     |      Raises:
     |          None.
     |
     |      Notes:
     |          This method displays the input image on a tkinter canvas with keyboard controls enabled. The user can enter a letter to filter the displayed 
text chunks by their first letter. Pressing the letter corresponding to the desired text chunk's first letter selects that chunk's coordinate location as the "selected_coordinate" variable. The selected coordinate is stored as a tuple in the format (x, y).
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  converted_image = None
     |
     |  coordinate_data = {}
     |
     |  image_path = None
     |
     |  original_image = None
     |
     |  processed_image = None
     |
     |  selected_coordinate = None
     |
     |  x = <main.system object>

    class system(builtins.object)
     |  system(fast=True)
     |
     |  A class to manage files and directories, create a number-based series of files, take screenshots, and interact with the mouse pointer.
     |
     |  Attributes:
     |      generalPath (str): The main path of the project.
     |      paths (dict): A dictionary containing paths of files and directories.
     |      directories (dict): A dictionary containing directories.
     |      folders (dict): A dictionary containing file extensions for different series folders.
     |
     |  Methods:
     |      __init__: Initializes the class instance.
     |      pathways(mainPath=None, files=True): Generates a nested structure representing directories and files in a given path.
     |      series(series, new=True, file=True): Helps to manage a number-based series of files within a specified directory.
     |      image(show=False): Takes a screenshot of the current screen and returns it as a PIL image.
     |      mouse(dataPoint): Moves the mouse pointer to a specified location of an element and then clicks it.
     |
     |  Methods defined here:
     |
     |  __init__(self, fast=True)
     |      Initializes the class instance.
     |
     |      Args:
     |          fast (bool): A boolean value indicating whether to use fast processing mode. Default is False.
     |
     |      Returns:
     |          None.
     |
     |  check(self)
     |
     |  image(self, show=False)
     |      Takes a screenshot of the current screen and returns it as a PIL image.
     |
     |      Args:
     |          show (str, optional): If specified, opens the image at the specified file path instead of taking a screenshot. Defaults to False.
     |
     |      Returns:
     |          tuple: A tuple containing first the file path and then the Pillow image.
     |
     |      Notes:
     |          To use pyautogui on Linux, run ```sudo apt-get install scrot```.
     |
     |  mouse(self, dataPoint)
     |      Moves the mouse pointer to a specified location of an element and then clicks it..
     |
     |      Args:
     |          dataPoint (list): A list containing either the (x, y) coordinates of a point or a sublist of text data in the format [left, top, right, bottom, confidence, text].
     |
     |      Returns:
     |          None.
     |
     |      Notes:
     |          The method uses the PyAutoGUI library to move the mouse pointer. The coordinates of the mouse pointer are scaled based on the current screen 
resolution.
     |
     |  series(self, series, new=True, file=True)
     |      Helps to manage a number-based series of files within a specified directory.
     |
     |      Args:
     |          series (str): The name of the series folder.
     |          new (bool, optional): If True, creates a new file or folder. If False, retrieves existing file versions. Defaults to True.
     |          file (bool, optional): If True, creates a file. If False, creates a folder. Defaults to True.
     |
     |      Returns:
     |          Union[str, List[str]]: If new is True, returns the full path to the newly created file or folder. If new is False, returns a list of full paths to existing files in the series.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |
     |  folders = {'data': '.pkl', 'docs': '.md', 'highlights': '.toml', 'hist...
     |
     |  generalPath = ''

FUNCTIONS
    exit(status=None, /)
        Exit the interpreter by raising SystemExit(status).

        If the status is omitted or None, it defaults to zero (i.e., success).
        If the status is an integer, it will be used as the system exit status.
        If it is another kind of object, it will be printed and the system
        exit status will be one (i.e., failure).

    main()
