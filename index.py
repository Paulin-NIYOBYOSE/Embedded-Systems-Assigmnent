import os
import time
import shutil
import subprocess

# Configure folder paths
camera_folder = "/path/to/camera/folder"  # Replace with the actual folder path
uploaded_folder = "/path/to/uploaded/folder"  # Replace with the actual folder path
upload_url = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"

# Ensure the uploaded folder exists
os.makedirs(uploaded_folder, exist_ok=True)


def upload_picture(file_path):
    """
    Upload a picture using the curl command.
    """
    try:
        # Execute the curl command
        response = subprocess.run(
            ["curl", "-X", "POST", "-F", f"imageFile=@{file_path}", upload_url],
            capture_output=True,
            text=True
        )
        if response.returncode == 0:
            print(f"Uploaded {file_path} successfully.")
            return True
        else:
            print(f"Failed to upload {file_path}. Response: {response.stderr}")
            return False
    except Exception as e:
        print(f"Error while uploading {file_path}: {e}")
        return False


def monitor_and_upload():
    """
    Monitor the folder, upload pictures, and move them to the uploaded folder.
    """
    while True:
        # Get all files in the camera folder
        files = [f for f in os.listdir(camera_folder) if os.path.isfile(os.path.join(camera_folder, f))]

        for file in files:
            file_path = os.path.join(camera_folder, file)

            # Wait for 30 seconds before uploading
            print(f"Waiting 30 seconds before uploading: {file}")
            time.sleep(30)

            # Attempt to upload the picture
            if upload_picture(file_path):
                # Move to uploaded folder after successful upload
                shutil.move(file_path, os.path.join(uploaded_folder, file))
                print(f"Moved {file} to {uploaded_folder}")

        # Sleep for a while before checking again
        time.sleep(10)


if __name__ == "__main__":
    monitor_and_upload()
