"""This file contains the class `GUI`, which is the primary interface for KeyFlare."""
import tempfile
import tkinter as tk
from tkinter import ttk
import tkinter.colorchooser as cc
import cv2
from .image_pipeline import ImagePipeline


class GUI:
    """
    This class named GUI (Graphical User Interface) serves as the
    primary interface for interacting with KeyFlare.
    It includes a coordinate selector, a keyboard input detector, color selector, etc.
    It continuously narrows down the location of your intended mouse
    click until it has been resolved, clicking automatically without a mouse.

    Attributes:
        root (Tk object): The root Tk window for the KeyFlare application.
        input_char (str): The character input by the user.
        y (ImagePipeline object): An instance of the
            ImagePipeline class used for image processing and coordinate finding.
        exit_flag (bool): Flag to indicate whether to
            exit the application or not by the Usages class.
        color (tuple): The selected input method's color represented in (R, G, B) format.
        label: A tk Label to be shown in the application.
        temp_name: Name of the temporary file.

    Methods:
        run(clicks: int): Runs KeyFlare's GUI process for selecting a coordinate.
        selecting_coordinate(clicks: int): Manages the
            process of selecting a coordinate on the keyboard image.
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
            clicks (int, required): The number of mouse
                clicks to perform when a place to click has been found.

        Returns:
            None

        Notes:
            - Users can press a key on their physical keyboard,
              and the GUI will respond by narrowing down the
              available key options based on the input character.
            - If no matching key is found, the GUI will display
              color selection options and allow the user to exit the application.

        Example:
            >>> gui = GUI()
            >>> gui.run(clicks=2)
        """
        self.y.run()
        self.root = tk.Tk()
        self.root.title("KeyFlare")
        self.root.wm_attributes("-fullscreen", True)
        self.root.attributes("-topmost", 1)
        self.root.focus_force()
        self.label = tk.Label().pack()
        self.selecting_coordinate(clicks)

    def selecting_coordinate(self, clicks):
        """
        Manages the process of selecting a coordinate on
        the keyboard image, clicking the point at the end
        or showing a preference menu at the end if no point was found.

        Args:
            clicks (int, required): The number of mouse clicks to
                perform when a place to click has been found.

        Returns:
            None

        Example:
            >>> gui = GUI()
            >>> gui.run(clicks=2) # Notice: please do not run this by itself
        """
        for _ in range(6):
            image = self.y.original_image.copy()
            if self.label:
                self.label.destroy()
            if self.root.winfo_exists():
                for key, loc in self.y.coordinate_data:
                    image = cv2.rectangle(
                        image,
                        (loc[0], loc[1]),
                        (loc[0] + 13 * len(self.y.coordinate_data[0][0]), loc[1] + 20),
                        self.color,
                        -1,
                    )
                    text_size, _ = cv2.getTextSize(key, cv2.FONT_HERSHEY_PLAIN, 0.75, 1)
                    image = cv2.putText(
                        image,
                        key,
                        (
                            loc[0]
                            + (10 * len(self.y.coordinate_data[0][0]) - text_size[0])
                            // 2,
                            loc[1] + (20 + text_size[1]) // 2,
                        ),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        0.75,
                        (0, 0, 0),
                        1,
                        cv2.LINE_AA,
                    )
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                _, buffer = cv2.imencode(".png", image)
                with tempfile.NamedTemporaryFile(
                    suffix=".png", delete=False
                ) as temp_file:
                    temp_file.write(buffer.tobytes())
                    self.temp_name = temp_file.name
                image = tk.PhotoImage(file=self.temp_name)
                self.label = ttk.Label(self.root, image=image)
                self.label.pack()
                self.root.update_idletasks()
                self.root.lift()
                self.root.focus_force()
                self.root.after(1, lambda: self.root.focus_force())
                self.root.attributes("-topmost", True)
                self.root.after_idle(self.root.attributes, "-topmost", False)
                self.root.focus_force()
                self.root.after(50, self.focus_window)
                self.root.bind("<Key>", self.on_key)
                self.root.grab_set()
                self.root.mainloop()
            if len(self.y.coordinate_data) == 1:
                self.root.destroy()
                self.y.x.mouse(
                    [
                        self.y.coordinate_data[0][1][0] + 10,
                        self.y.coordinate_data[0][1][1] + 10,
                    ],
                    clicks=clicks,
                )
                break
            if len(self.y.coordinate_data) == 0:
                self.root.quit()
                self.label.destroy()
                style = ttk.Style()
                style.theme_use("classic")
                label_frame = ttk.Frame(self.root, padding=20)
                label_frame.pack(fill="both", expand=True)
                self.label = ttk.Label(
                    label_frame,
                    text="Selected color:",
                    font=("Arial", 14),
                    background=self.rgb_to_hex(self.color),
                    foreground="#000000",
                )
                self.label.pack()
                select_button = ttk.Button(
                    self.root, text="Select Color", command=self.select_color
                )
                select_button.pack(pady=10)
                exit_button = ttk.Button(
                    self.root, text="Completely Exit KeyFlare", command=self.exit_app
                )
                exit_button.pack(pady=10)
                pass_button = ttk.Button(
                    self.root,
                    text="Continue (or Press Any Key)",
                    command=self.root.destroy,
                )
                pass_button.pack(pady=10)
                self.root.bind("<Key>", lambda e: self.root.destroy())
                self.root.mainloop()
                break

    def on_key(self, event):
        """
        Filters and updates available key options on a keyboard input event.
        Narrows down the choices to find the spot to click.

        Args:
            event (tkinter.Event): The keyboard event containing information about the pressed key.

        Returns:
            None

        Example:
            To use this method, you can define it as an
            event handler for a tkinter window like this:
            >>> self.root.bind("<Key>", self.on_key)
        """
        self.input_char = event.char
        self.y.coordinate_data = [
            (key[len(self.input_char) :], p1)
            for key, p1 in self.y.coordinate_data
            if key[0].lower() == self.input_char.lower()
        ]
        self.root.quit()

    def exit_app(self):
        """
        For exiting the KeyFlare application gracefully.
        It sets an exit flag and closes the application window.

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
        Opens a color selection dialog and updates the
        selected color in the GUI. The selected color is
        then displayed in the GUI, and the RGB values are updated.

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
            if isinstance(color, str) and color.startswith("#"):
                color = tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))
            self.color = tuple(map(int, color))
            self.label.config(
                text=f"Selected color: {self.color}",
                background=self.rgb_to_hex(self.color),
            )

    def rgb_to_hex(self, rgb):
        """
        Converts an RGB color tuple to its hexadecimal representation.

        Args:
            rgb (tuple): A tuple containing three integers
                representing the red, green, and blue color channels, respectively.

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
        Sets the application window to the foreground and ensures it has focus,
        no matter what. It is against the purpose of the application
        to find you have to use your mouse to click the image shown.

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
        self.root.attributes("-topmost", True)
        self.root.after_idle(self.root.attributes, "-topmost", False)
        self.root.focus_force()
