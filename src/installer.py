import os, subprocess
from esp_utils import hard_reset

print("GRADES CALCULATOR ESP32 INSTALLER V1.0")
print("Step 1/2: Checking for files...")
files = os.listdir(os.getcwd())
try:
    files.pop(files.index("installer.py"))
    
    files.pop(files.index("main.py"))
    files.pop(files.index("main_esp32.py"))
    files.pop(files.index("esp_utils.py"))
    files.pop(files.index("connector_app.py"))
    # we dgaf if __pycache__ ain't there zro
    try:
        files.pop(files.index("__pycache__"))
    except:
        pass

    # and also this
    try:
        files.pop(files.index("grades_report"))
    except:
        pass
except Exception as e:
    print(f"Error while setting up installer enviroment!")
    print(f"Error:\n{e}")
    exit(1)
finally:
    files.insert(0, "main_esp32.py")
    for i in files:
        if not os.path.exists(i):
            print(f"File {i} doesn't exist! Make sure it exists at {os.getcwd()}")
            exit(1)

print("Step 2/2: Checking for device...")
def check():
    def no_device_connected_error() -> None:
        print("No device connected, make sure that the remote device has micropython installed!")
        exit(1)

    try:
        output = subprocess.check_output(['mpremote', 'devs'], stderr=subprocess.STDOUT, timeout=2)
    except subprocess.CalledProcessError as e:
        output = e.output
        
    if output.decode().lower().replace(" ", "").replace("\n", "").replace("\r", "") == "":
        no_device_connected_error()

check()
print("Finished checking, Device found! Beginning installation!!!")
print("DO NOT TURN OFF DEVICE!!")

for index, file in enumerate(files):
    if "main_esp32.py" in file:
        print(f"Copying main program!, {index+1} / {len(files)}")
        command = f"mpremote cp {file} :main.py"
    else:
        print(f"Copying file: {file}, {index+1} / {len(files)}")
        command = f"mpremote cp {file} :{file}"
    
    try:
        subprocess.run(command.split(), capture_output=True, text=False)
    except ChildProcessError as e:
        print(f"An error occured while copying: {file}:")
        print(e)
        exit(1)

print("FINISHED INSTALLATION!! RESETTING...")
hard_reset(is_transfermode=False)
