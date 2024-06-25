import os
import shutil
import subprocess

def stop_apache():
    try:
        subprocess.run(['systemctl', 'stop', 'apache2'], check=True)
        print("Apache server stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop Apache server: {e}")

def start_apache():
    try:
        subprocess.run(['systemctl', 'start', 'apache2'], check=True)
        print("Apache server started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Apache server: {e}")

def upload_files(source_dir, destination_dir, files):
    try:
        for file in files:
            source_file = os.path.join(source_dir, file)
            destination_file = os.path.join(destination_dir, file)

            if os.path.exists(source_file):
                shutil.copy2(source_file, destination_file)
                print(f"Uploaded {file} to {destination_dir}")
            else:
                print(f"Source file does not exist: {source_file}")

    except Exception as e:
        print(f"An error occurred while uploading files: {e}")

def set_permissions(destination_dir):
    try:
        submissions_dir = os.path.join(destination_dir, 'submissions')
        if not os.path.exists(submissions_dir):
            os.makedirs(submissions_dir)
            print(f"Created directory: {submissions_dir}")

        # Change ownership to www-data (Apache user)
        subprocess.run(['chown', '-R', 'www-data:www-data', submissions_dir], check=True)
        print(f"Changed ownership of {submissions_dir} to www-data")

        # Set permissions
        subprocess.run(['chmod', '-R', '775', submissions_dir], check=True)
        print(f"Set permissions for {submissions_dir} to 775")

    except subprocess.CalledProcessError as e:
        print(f"Failed to set permissions: {e}")

if __name__ == '__main__':
    source_directory = '/home/kali/Desktop'  # Change this to your source directory
    destination_directory = '/var/www/html'
    files_to_upload = ['index.html', 'boxsite.html', 'submit.php']  # Add submit.php to the list of files

    # Stop Apache server
    stop_apache()

    # Upload files
    upload_files(source_directory, destination_directory, files_to_upload)

    # Set permissions
    set_permissions(destination_directory)

    # Start Apache server
    start_apache()
