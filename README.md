# Simple Weather Fetcher

## Purpose

`get_weather.py` is a Python script that fetches and displays weather information from the command line using the [wttr.in](https://wttr.in/) service. It prompts the user for a location and then uses `curl` to retrieve the weather report.

## Prerequisites

Before running this script, you must have `curl` installed on your system. `curl` is a command-line tool for transferring data with URLs, and this script relies on it to fetch weather data.

### Checking for `curl`

You can typically check if `curl` is installed by opening your terminal or command prompt and typing:
```bash
curl --version
```
If `curl` is installed, this command will display its version. If not, you'll likely see an error message indicating the command was not found.

### Installing `curl`

- **On Debian/Ubuntu-based Linux:**
  ```bash
  sudo apt update && sudo apt install curl
  ```
- **On Fedora/RHEL-based Linux:**
  ```bash
  sudo dnf install curl
  ```
  or
  ```bash
  sudo yum install curl
  ```
- **On macOS (often pre-installed):**
  If not present, you can install it using Homebrew:
  ```bash
  brew install curl
  ```
- **On Windows:**
  `curl` is included with Windows 10 and later versions. You can also get it by installing Git for Windows, which bundles `curl`.

## How to Run

1.  **Save the script:** Make sure you have the `get_weather.py` script saved on your system.
2.  **Open your terminal or command prompt.**
3.  **Navigate to the directory** where you saved `get_weather.py`.
    ```bash
    cd path/to/script_directory
    ```
4.  **Run the script** using Python:
    ```bash
    python get_weather.py
    ```
5.  **Enter your location:** The script will prompt you to enter a location. Type the name of a city (e.g., "London", "Paris", "New York") or a specific area and press Enter.
6.  **View the weather:** The script will then display the weather report for the specified location.

### Example
```bash
python get_weather.py
Enter your location: Tokyo
```
The script will then output the weather information for Tokyo.

## Error Handling

The script includes basic error handling for:
-   `curl` not being installed.
-   The specified location not being found by `wttr.in`.
-   Other issues during the data fetching process (e.g., network problems).

If you encounter any issues, ensure `curl` is correctly installed and that you have an active internet connection.
