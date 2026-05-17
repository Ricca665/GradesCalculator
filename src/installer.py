import os, subprocess, shutil
from esp_utils import hard_reset
import sys
import random
import zipfile, time
from rich.progress import Progress

print("GRADES CALCULATOR ESP32 INSTALLER V1.0")
args = sys.argv
if len(args) <= 1:
    print(f"You forgot to parse the install package as a parameter {"you fucking buffoon" if random.random() > 0.45 else ""}")
    exit(1)

file = args[1]

print("Step 1/2: Checking for files...")
if not os.path.exists(file):
    print(f"Package file {file} doesn't exist!")
    exit(1)

if not ".zip" in file:
    print("File is not zip file!")
    exit(1)

with zipfile.ZipFile(file, "r") as zip_ref:
    zip_ref.extractall("package_dir")

os.chdir("package_dir")
files = os.listdir(".")

def exit(code=0):
    # clean up the mess
    print("Cleaning up...")
    os.chdir("..")
    shutil.rmtree("package_dir", True)

    sys.exit(code)

try:
    # shift array so the first element is always the main program
    index = files.index("main.py")
    value = files[index]
    files.pop(index)
    files.insert(0, value)
except ValueError:
    print("Main program not found in package! Exiting...")
    exit(1)

print("Step 2/2: Checking for device...")
def no_device_connected_error() -> None:
    print("No device connected, make sure that the remote device has micropython installed!")
    exit(1)

# we check the output coming from mpremote, if it's blank then we know that no device is plugged in
try:
    output_stdout = subprocess.check_output(['mpremote', 'devs'], stderr=subprocess.STDOUT, timeout=2)
except subprocess.CalledProcessError as e:
    output_stdout = e.output
        
if output_stdout.decode().lower().replace(" ", "").replace("\n", "").replace("\r", "") == "":
    no_device_connected_error()

# weird logic, but it boils down to these steps
# if mpremote manages to connect to the remote device that means it's going to be connected for longer (aka indefenetly)
# which means that it's going to trigger the timeout expired
# if it instead doesn't do that aka displays a no device connected error, we automatically know
# with some safety checks ofc, that it didn't connect since the timeout didn't trigger
try:
    output_stdout = subprocess.check_output(["mpremote"], stderr=subprocess.STDOUT, timeout=3)
    no_device_connected_error()
except subprocess.TimeoutExpired:
    time.sleep(1)
    output_stdout = None

if output_stdout != None:
    if "no device" in output_stdout.decode():
        no_device_connected_error()
    
# clean up the mess i guess?
time.sleep(1.25)
for _ in range(3):
    subprocess.run(["mpremote", "reset"], capture_output=True, text=True)
    time.sleep(1.25)

print("Finished checking, device found! Beginning installation!!!")
print("DO NOT TURN OFF DEVICE!!")

def copy(file:str) -> None:
    file_abs = os.path.abspath(file).replace("\\", "/")
            
    if "main.py" in file:
        print(f"Copying main program!, {index+1} / {len(files)}")
                
    else:
        print(f"Copying file: {file}, {index+1} / {len(files)}")
            
    time.sleep(1)
    command = ["mpremote", "cp" , file_abs, f":{file}"]
    #print(command)
    try:
        command_result = subprocess.run(command, capture_output=True, text=True)
        output_stdout = command_result.stdout
        output_stderr = command_result.stderr
    except Exception as e:
        output_stdout = None
        output_stderr = None
        print(f"An error occured while copying: {file}:")
        print(e)
        exit(1)

    if output_stdout != None and output_stderr != None:
        if "error" in output_stdout.lower() or "exception" in output_stdout.lower() or "error" in output_stderr.lower() or "exception" in output_stderr.lower():
            print("An error has occured while copying:")
            print(output_stdout)
            exit(1)
                
with Progress() as p:
    t = p.add_task("Copying...", total=len(files))
    for index, file in enumerate(files):
        copy(file)
        p.update(t, advance=1)
        time.sleep(1)
    

print("FINISHED INSTALLATION!! RESETTING...")
hard_reset(is_transfermode=False, exit_after_reset=False)

print("Done!")
exit()
