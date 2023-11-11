# KeyFlare
[![Downloads](https://static.pepy.tech/badge/keyflare)](https://pepy.tech/project/keyflare)
[![Website](https://img.shields.io/website-up-down-green-red/http/monip.org.svg)](https://www.pranitshah.cyou/keyflare)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## About
Some users prefer using a keyboard over a mouse because of accessibility needs or personal reasons. KeyFlare enables users to interactively control their mouse using their keyboard.  Showcases available on my [website](https://www.pranitshah.cyou/keyflare). KeyFlare is open source, free, and both easy to understand and install.

Also, please check the documentation in [github wiki](https://github.com/pranitsh/keyflare/wiki)!

![An example image of KeyFlare in action](images/Screenshot.jpg)

## Installation

Suggested:
```sh
pip install keyflare
keyflare
```

Alternative 1:
```sh
pip install -e git+https://github.com/pranitsh/keyflare.git@main#egg=keyflare --upgrade
```
- The `@main` installs the main branch.
- The `#egg=keyflare` makes sure to name the package keyflare
- The `--upgrade` forces an update to the library if you had it installed already somehow through another package that depends on it or something else.
- The `-e` means that the source code is installed too. The logging done when you run this line (normally the second line from the top) will show you where it is. You can then edit this source code for changes to propagate to the library. I do not often use this feature, but it is there for others if you want it.

```sh
pip install -e "git+https://github.com/pranitsh/keyflare.git@main#egg=keyflare[dev]" --upgrade
```
- Add the quotation marks and the `[dev]` for the developer toolkit to come with it (including pytest, wheel, etc)


Alternative 2:
- Use `git clone https://github.com/pranitsh/keyflare.git` to install the source code
- Optional: create a virtual environment with `python -m venv env` and activate it as per your system
- Install dependencies: `pip install -r requirements.txt`
- Go to the KeyFlare root directory and run `python keyflare`, which will run the code in `__main__.py` automatically.

For macOS, both PyAutoGUI (which takes screenshots and moves the mouse) and pynput (which monitors keyboard for hotkey) do claim compatibility with macOS. However, there are some macOS-specific hoops you should be aware of:
- pynput requires `sudo keyflare` and on macOS versions post-Mojave, you may need to whitelist your terminal application
- PyAutoGUI requires users on El Capitan to run `MACOSX_DEPLOYMENT_TARGET=10.11 pip install pyobjc`

### Inspiration

Vimium C, a common tool for users with accessibility needs for navigating web browsers, does not work on web browsers. Apple Voice Control's smart grid, a tool for navigating on Apple displays, does not work outside of an iPhone and would not be effective on large displays. There was no tool available for this, so I decided to make it.

### Features

- Intuitive Hotkey: (Left Alt) + (Lowercase A)
- Intuitive Process: KeyFlare simply opens up a fullscreen image to show you the options on the screen.
- Enhanced image segmentation algorithm that optimizes speed.
- Cross-platform compatibility with Linux, macOS, and Windows. (Untested on macOS since I do not have access to that environment at the moment.)

#### In the works

- Specifying the number of clicks desired through preferences.
- Making it easier to use KeyFlare through imports by improving the documentation.

**[Please fill out the survey](https://forms.gle/AVNGoHaFzGwHcsMz8)**
