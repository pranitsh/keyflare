[![Build KeyFlare executables](https://github.com/Pshah2023/keyflare/actions/workflows/main.yml/badge.svg)](https://github.com/Pshah2023/keyflare/actions/workflows/main.yml)
# KeyFlare 
## About
KeyFlare is a useful tool that enables users to interactively control their mouse using their keyboard. KeyFlare can provide an expanded user experience for those who prefer to use a keyboard over a mouse. Showcases available soon on week 5 (old showcases available on week 2 and 3) of my [senior project page](https://sites.google.com/email.medfield.net/psp/0?authuser=0).

### Features

- Intuitive keyboard-based mouse control: KeyFlare shows a list of coordinates representing UI elements on your screen that you can click on by typing the unique alphabetical identifier for a coordinate of interest. 
- Improved hotkeys: Initating KeyFlare with Left Alt+A+Z combination will click the screen once at the end while the right Alt+A+Z combination will click the screen twice.
  - Inputs arguments let you define the number of clicks when run from terminal
- Customizable user experience: A preferences window allows users to change the background color, exit the application, or exit just the current process (or by pressing Return).
- Enhanced image segmentation algorithm that optimizes speed.
- Cross-platform compatibility with Linux, macOS, and Windows: all desktop environments!

## Installation

### For all users

- Download and run the latest KeyFlare binary from the the [releases](https://github.com/Pshah2023/keyflare/releases/).
  - Although I am an unverified developer, you can ignore those warnings. I plan to solve this problem in the near future.
 
#### For linux users
- Try the binary. If something doesn't work, refer to these steps.
- You may have to make the script executable first before you can run it.
- You may need to connect a system hotkey to the command `/path/to/keyflare 1` (the number represents the number of clicks) since pynput's keyboard library may not work on wayland-based systems.

#### Developers

- Use `git clone https://github.com/Pshah2023/keyflare.git` to install the source code
- Run in terminal `bash keyflare/run.sh install` to download prerequisite libraries and help develop the product


**[Please fill out the survey](https://forms.gle/VtxPTN4WKMyU4uwV9)**