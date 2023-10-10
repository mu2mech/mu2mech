# mu2mech

mu2mech is a multiscale phase field modeling software designed for Linux-based systems. This README provides instructions for installing and running the software.

## Required Libraries and Modules

### Python Modules
- numpy
- pyside2
- pyvista
- pyvistaqt
- matplotlib
- ffmpeg-python
- pyyaml

### Other Libraries
- ffmpeg

## Installation Instructions

Follow the steps below to install and run mu2mech on your Ubuntu system:

1. **Download files** 

- Download or clone the repository

    Click Code->Download ZIP

    Or

    In terminal type command 
    ```
    git clone https://github.com/mu2mech/mu2mech
    ```

2. **Install python and pip package manager**
    ```
    sudo apt install python3
    sudo apt install python3-pip
    ```


3. **Create and activate a Python environment:**
   - Open a terminal and execute the following commands:
     ```bash
     python3 -m venv mu2mech-env
     source mu2mech-env/bin/activate
     ```

4. **Install packages:**
   - Install Python packages:
     ```bash
     pip install -r requirements.txt
     ```
   - Install the ffmpeg library:
     ```bash
     sudo apt install ffmpeg
     ```

5. **Run the program:**
   - Activate environment if not activated
      ```bash
      source mu2mech-env/bin/activate
      ```
   - Execute the following command:
     ```bash
     python3 mu2mech.py
     ```

## Troubleshooting

If you encounter any errors during the installation or execution of mu2mech, refer to the following solutions:

- **ImportError: libOpenGL.so.0: cannot open shared object file: No such file or directory**
  - Resolve this issue by installing the libopengl0 package:
    ```bash
    sudo apt install libopengl0 -y
    ```

- **qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.**
  - Reinstall the libxcb-xinerama0 package to fix this problem:
    ```bash
    sudo apt-get install --reinstall libxcb-xinerama0
    ```
