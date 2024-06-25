import subprocess
import threading
import time

# List of scripts to run
scripts = ['cloner.py', 'desk.py', 'modifier.py', 'my_flask_app/uploadflask.py']

print("Running script:", scripts[0])
subprocess.run(['python', scripts[0]])

print("Running script:", scripts[1])
subprocess.run(['python', scripts[1]])

print("Running script:", scripts[2])
subprocess.run(['python', scripts[2]])

#print("Running script:", scripts[3])
#subprocess.run(['python', scripts[3]])

