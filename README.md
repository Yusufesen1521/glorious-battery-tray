# Glorious Battery Tray

A lightweight, standalone Windows system tray application to display the real-time battery level of your Glorious Model I2 Wireless mouse.

![screenshot](https://i.imgur.com/r6H5yYy.png) ## Features

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

## Easy Installation (Recommended)

For most users, installing the standalone `.exe` is the easiest method.

1.  Go to the [**Releases Page**](https://github.com/YOUR_USERNAME/glorious-battery-tray/releases).
    *(Note: Replace `YOUR_USERNAME` with your actual GitHub username)*
2.  Download the `Glorious.exe` file from the latest release.
3.  Move the downloaded `Glorious.exe` to a permanent folder on your computer (e.g., create a folder in `C:\Program Files\GloriousBatteryTray`).
4.  Double-click `Glorious.exe` to run the application. The battery icon will appear in your system tray.

## Installation from Source (For Developers)

This method is for users who want to run the script directly using Python.

### Prerequisites

-   Windows 10 or 11
-   Python 3.x installed (make sure to check "Add Python to PATH" during installation).

### Steps

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/YOUR_USERNAME/glorious-battery-tray.git](https://github.com/YOUR_USERNAME/glorious-battery-tray.git)
    cd glorious-battery-tray
    ```
    (Alternatively, you can download the project as a ZIP file and extract it.)

2.  **Install the required libraries:**
    Open a terminal or Command Prompt in the project folder and run:
    ```sh
    pip install -r requirements.txt
    ```

3.  **Run the script:**
    ```sh
    python Glorious.py
    ```

## Running on Startup (Optional)

To make the application run automatically when you start your computer:

1.  Press `Win + R` to open the Run dialog.
2.  Type `shell:startup` and press Enter. This will open the Startup folder.
3.  Create a shortcut to the application in this folder.
    -   **For the .exe version**: Right-click and drag your `Glorious.exe` file into the Startup folder and select "Create shortcuts here".
    -   **For the script version**: Right-click inside the Startup folder, go to `New > Shortcut`. In the "location" field, enter `pythonw.exe "C:\path\to\your\Glorious.py"`. Using `pythonw.exe` will prevent a console window from appearing.

## Creating the Executable (For Contributors)

To create a standalone `.exe` from the source code, you'll need `pyinstaller`.

1.  **Install PyInstaller:**
    ```sh
    pip install pyinstaller
    ```
2.  **Build the .exe:**
    Run the following command in the project's root directory. An icon file named `app.ico` is recommended.
    ```sh
    pyinstaller --onefile --windowed --icon="app.ico" Glorious.py
    ```
3.  The final `Glorious.exe` will be located in the `dist` folder.

## Troubleshooting

-   **Device Not Found**: Ensure your Glorious Model I2 Wireless mouse is connected (either via dongle or cable). The script is specifically configured for `VENDOR_ID = 0x093a` and `PRODUCT_ID = 0x821d`.
-   **Logs**: The application creates a log file at `C:\Users\YOUR_USERNAME\Documents\GloriousBatteryMonitor\battery_tray_app.log`. Check this file for detailed error information.