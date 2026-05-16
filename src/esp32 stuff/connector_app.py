import subprocess, sys, os, time
import diary_utils
from esp_utils import *

def check_for_device():
    print("Checking for device...")
    def no_device_connected_error() -> None:
        print("No device connected, make sure in settings that the device is plugged in and that\ntransfer to device option is selected")
        exit(1)

    try:
        output = subprocess.check_output(['mpremote', 'devs'], stderr=subprocess.STDOUT, timeout=2)
    except subprocess.CalledProcessError as e:
        output = e.output
    
    if output.decode().lower().replace(" ", "").replace("\n", "").replace("\r", "") == "":
        no_device_connected_error()

    try:
        output = subprocess.run(['mpremote'], timeout=3, capture_output=True, text=True).stdout
    except subprocess.CalledProcessError as e:
        no_device_connected_error()
    except subprocess.TimeoutExpired as e:
        output = str(e.stdout)
        if output == None or output.count("\n") < 5 or "DETACH" not in output:
            print("Device is not in transfer mode!")
            print("Please put device in transfer mode via settings")
            exit(1)
            
    subprocess.run(["mpremote", "reset"], capture_output=True, text=False)
    print("Device checked, continuing...")

oginput = input
def input(str="") -> str:
    try:
        return oginput(str)
    except (KeyboardInterrupt, EOFError):
        print("\nexiting...")
        hard_reset()
        sys.exit()

inp = None
grades_path = f"{os.getcwd()}/grades.ini"

print("Configuring device...")
print("Step 1/2: Device verification...")
check_for_device()

print("Step 2/2: Configuring device's clock...")
subprocess.run(["mpremote", "reset"], capture_output=True, text=False)
subprocess.run(["mpremote", "rtc", "--set"], capture_output=True, text=False)
subprocess.run(["mpremote", "reset"], capture_output=True, text=False)

print("Finished configuring device.")

while inp != "exit":
    print("Select option:")
    print("1. Transfer grades to device")
    print("2. Transfer grades from device")
    print("3. Erase grades on device")
    print("4. Exit transfer mode")
    inp = input().lower()
    
    if inp.isdigit():
        inp = int(inp)
        match inp:
            case 1 | 2:
                if not os.path.exists(grades_path) and inp == 1:
                    print("No grades exists on current device")
                    continue

                if inp == 2 and os.path.exists(grades_path): # only run backup just in case we are copying FROM the device
                    diary_utils.backup_grades()

                check_for_device()
                subprocess.run(["mpremote", "reset"], capture_output=True, text=False)
                time.sleep(1)
                print("Beginning copying. DO NOT TURN OFF DEVICE!!!")
                err = False
                try:
                    # 1: we are copying to the device
                    # 2: we are copying from the device
                    if inp == 1:
                        subprocess.check_output(["mpremote", "cp", grades_path, ":grades.ini"])
                    else:
                        subprocess.check_output(["mpremote", "cp", ":grades.ini", grades_path])
                except:
                    print("Failed to copy grades")
                    err = True
                
                if not err:
                    print("Finished copying grades")
                    hard_reset()
            case 3:
                choice = ""
                while choice.lower() != "y" and choice.lower() != "n":
                    choice = input("ARE YOU SURE? THIS PROCESS IS IRREVERSIBLE! (y/N) ")
                if choice.lower() == "n":
                    print("Not erasing grades!")
                    continue
                elif choice.lower() == "y":
                    check_for_device()
                    print("ERASING GRADES!!!!!!!!")
                    print("DO NOT TURN OFF DEVICE!!!!")
                    print("Erasing...")    
                    subprocess.run(["mpremote", "reset"], capture_output=True, text=False)
                    time.sleep(1)
                    err = False
                    try:
                        subprocess.check_output(["mpremote", "rm", "-rv", ":grades.ini"])
                    except:
                        print("Failed to erase grades")
                        err = True
                    
                    if not err:
                        print("Finished erasing grades.")
                        hard_reset()
            case 4:
                check_for_device()
                subprocess.run(["mpremote", "reset"], capture_output=True, text=False)
                time.sleep(1)

                print("Changing device state...")
                hard_reset()

hard_reset()
