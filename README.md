# Glorious Battery Tray

A lightweight, standalone Windows system tray application to display the real-time battery level of your Glorious Model I2 Wireless mouse.


-   **Real-Time Monitoring**: See your mouse's battery percentage directly in your system tray.
-   **Dynamic Icon**: The tray icon is a number that updates automatically.
-   **Color-Coded Levels**:
    -   **Green (`> 75%`)**: Battery is high.
    -   **White (`21% - 75%`)**: Battery is normal.
    -   **Red (`<= 20%`)**: Low battery warning.
-   **Status Indicators**: Shows `...` when connecting and `X` if the device is disconnected.
-   **Lightweight**: Minimal resource usage, runs quietly in the background.
-   **Auto-Reconnect**: Automatically tries to reconnect if the mouse is turned off or goes to sleep.
-   **No External Software Needed**: Doesn't require Glorious Core to be running.

## Installation

### Prerequisites

-   Windows 10 or 11
-   Python 3.x installed (make sure to check "Add Python to PATH" during installation).

### Steps

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/YOUR_USERNAME/glorious-battery-tray.git](https://github.com/YOUR_USERNAME/glorious-battery-tray.git)
    cd glorious-battery-tray
    ```
    (You can also download the project as a ZIP file and extract it.)

2.  **Install the required libraries:**
    Open a terminal or Command Prompt in the project folder and run:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

You can either run the application directly as a Python script or compile it into a standalone `.exe` file for easier use.

### Method 1: Running as a Script

In your terminal, simply run the following command:

```sh
python Glorious.py
```
The battery icon will appear in your system tray.

### Method 2: Creating a Standalone `.exe` File

This method packages the application into a single executable file, so you don't need to run it from a terminal every time.

1.  **Install PyInstaller:**
    If you don't have it installed, run this command:
    ```sh
    pip install pyinstaller
    ```

2.  **Build the Executable:**
    In the project's root directory, run the following command. An icon file named `app.ico` is recommended to be in the same folder for a custom icon.
    ```sh
    pyinstaller --onefile --windowed --icon="app.ico" Glorious.py
    ```
    -   `--onefile`: Bundles everything into a single `.exe`.
    -   `--windowed`: Prevents a command prompt window from opening when you run the app.

3.  **Run the App:**
    The finished `Glorious.exe` will be in a new folder called `dist`. You can move this file anywhere on your computer (e.g., to your Desktop or a folder in `Program Files`) and double-click it to start.

## Running on Startup (Optional)

To make the application run automatically when you start your computer:

1.  Press `Win + R` to open the Run dialog.
2.  Type `shell:startup` and press Enter. This will open the Startup folder.
3.  Create a shortcut to the application in this folder.
    -   **For the `.exe` version**: Right-click and drag the `Glorious.exe` file you created into the Startup folder and select "Create shortcuts here".
    -   **For the script version**: Right-click inside the Startup folder, go to `New > Shortcut`. In the "location" field, enter `pythonw.exe "C:\path\to\your\Glorious.py"`. Using `pythonw.exe` is important as it prevents a console window from appearing.

## Troubleshooting

-   **Device Not Found**: Ensure your Glorious Model I2 Wireless mouse is connected (either via dongle or cable). The script is specifically configured for `VENDOR_ID = 0x093a` and `PRODUCT_ID = 0x821d`.
-   **Logs**: The application creates a log file at `C:\Users\YOUR_USERNAME\Documents\GloriousBatteryMonitor\battery_tray_app.log`. Check this file for detailed error information.
