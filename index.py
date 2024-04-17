import subprocess
import datetime
import sys
import os

def send_file_to_api(url, file_path):
    try:
        # Generate timestamp for the log file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


        log_directory = "C:/traces"
        os.makedirs(log_directory, exist_ok=True)
        log_filename = os.path.join(log_directory, f"curl_log_{timestamp}.txt")

        # Run curl command to send the file to the API endpoint
        with open(log_filename, "w") as log_file:
            # Execute curl command to send file and capture response
            result = subprocess.run(["curl", "-X", "GET", url, "-F", f"file=@{file_path}"], stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True)

            # Write curl response to log file
            log_file.write("Curl Command Response:\n\n")
            log_file.write(result.stdout)

            print(f"Curl command executed successfully. Log saved to {log_filename}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Check if both arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python curl_script.py <API_URL> <FILE_PATH>")
        sys.exit(1)

    api_url = sys.argv[1]
    file_path = sys.argv[2]
    send_file_to_api(api_url, file_path)
