import shutil
import os
import stat

def copy_file_to_desktop():
    # Define the source file path and the destination directory
    source_file = '/root/.set/index.html'
    destination_dir = '/home/kali/Desktop'
    destination_file = os.path.join(destination_dir, 'index.html')

    try:
        # Ensure the source file exists
        if not os.path.exists(source_file):
            print(f"Source file does not exist: {source_file}")
            return

        # Ensure the destination directory exists
        if not os.path.exists(destination_dir):
            print(f"Creating destination directory: {destination_dir}")
            os.makedirs(destination_dir)

        # Copy the file to the desktop
        shutil.copy2(source_file, destination_file)
        print(f"File copied to {destination_file}")

        # Change the file permissions to make it publicly accessible
        os.chmod(destination_file, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        print(f"File permissions changed to make it publicly accessible")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    copy_file_to_desktop()
