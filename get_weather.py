import subprocess
import shutil

def is_curl_installed():
    """Check if curl is installed."""
    return shutil.which("curl") is not None

def get_weather():
    if not is_curl_installed():
        print("Error: curl is not installed. Please install curl to use this script.")
        return

    location = "NotARealPlace123xyz" # Hardcoded for testing unknown location
    location = input("Enter your location: ")
    if not location:
        print("Location cannot be empty.")
        return

    try:
        # Construct the command
        command = ["curl", f"wttr.in/{location}"]

        # Execute the command
        # Using subprocess.run for simplicity
        result = subprocess.run(command, capture_output=True, text=True, check=False)

        if result.returncode == 0:
            output = result.stdout
            # More robust check for unknown location, case-insensitive
            if "404 unknown location" in output.lower():
                print(f"Error: Could not find weather information for '{location}'. Please check the location name.")
            # Only print weather report if location was found
            else:
                print("\nWeather Report:\n")
                print(output)
        else:
            # Handle curl errors (e.g., network issues, invalid curl options)
            print(f"Error fetching weather data. curl exited with status {result.returncode}.")
            if result.stderr:
                print(f"Details: {result.stderr.strip()}")

    except FileNotFoundError:
        # This exception is technically covered by is_curl_installed,
        # but good to keep as a fallback.
        print("Error: curl command not found. Please ensure curl is installed and in your PATH.")
    except subprocess.TimeoutExpired:
        print("Error: The command timed out.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    get_weather()
