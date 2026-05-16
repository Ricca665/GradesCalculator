import grades_utils
import diary_utils
import sys
import time
try:
    import network # pyright: ignore[reportMissingImports]
    import time
    print("Initializing networking...")
    sta_if = network.WLAN(network.STA_IF); sta_if.active(True)

except:
    print("no esp32?")
    exit()

from number_utils import is_valid_number

features = True
inp = ""
oginput = input

try:
    import numpy as np
    import matplotlib.pyplot as plt
    from time import gmtime, strftime
except:
    try:
        from ulab import numpy as np # type: ignore
    except:
        import numpy as np
    features = False

def input(str="") -> str:
    try:
        return oginput(str)
    except (KeyboardInterrupt, EOFError):
        print("\nexiting...")
        sys.exit()

def mpremote_connection() -> None:
    while True:                     
        print("DETACH MPREMOTE NOW\r")
        print("\r\r\r\r\r\r\r\r")
        time.sleep(0.5)

diary_utils.init_diary()

try:
    print("Checking for transfer mode")
    with open("connection", "r") as f:
        ...
    mpremote_connection()
except:
    print("No transfer mode")
    pass

while inp != "exit":
    inp = input("[grades]> ").lower()
    if inp == "help":
        print("help: display this help guide")
        print("calculate grade (cg): yknow")
        print("check mininum grade (cmg): yknow")
        print("write to diary (wd): yknow")

    elif inp == "calculate grade" or inp == "cg":
        grades = grades_utils.input_grades(add_list_option=True)
        print(f"Grade: {grades_utils.grades_calculator(grades):.2f}")

    elif inp == "check mininum grade" or inp == "cmg":
        grades = grades_utils.input_grades(add_list_option=True)
        minimum_grade_to_fail = None
            
        for i in np.arange(10, -0.25, -0.25):
            temp_grades = grades.copy()
            temp_grades.append(i)    
            grade = grades_utils.grades_calculator(temp_grades)

            if (grade < 6):
                minimum_grade_to_fail = i
                break
                
        if (minimum_grade_to_fail != None):
            print("Minimun grade to fail: ", minimum_grade_to_fail)
        else:
            print("No grade can make you fail ig lmao")
    elif inp == "write to diary" or inp == "wd":
        diary_utils.write_grade(input("Insert subject name: ").lower(), grades_utils.input_grades())
    elif inp == "settings":      
        setting = ""
        while setting != "exit":
            print("1. Network Settings")
            print("2. Version information")
            print("3. Connect to connector app")
            print("Type exit to exit settings")
            setting = input("[grades] settings> ").lower()

            if setting.isdigit():
                setting = int(setting)
                if setting == 1:

                    print("Scanning networks...")

                    networks = []
                    for i in sta_if.scan():
                        ssid,_,_,_,_,_ = i
                        networks.append(ssid.decode("utf-8"))
                    
                    print("Choose network to connect to:")
                    for index, ssid in enumerate(networks):
                        print(index, ssid)
                    print("select network to connect to")
                    network_choose = ""

                    while not network_choose.isdigit():
                        network_choose = input().lower()
                    
                    network_choose = int(network_choose)
                    if network_choose < 0 or network_choose >= len(networks):
                        print("invalid network!")
                        continue

                    password = input("Insert password for network: ")
                    print("Connecting...")
                    sta_if.connect(networks[network_choose], password)
                    connected = False
                    time.sleep(3)
                    
                    for i in range(20):
                        if sta_if.isconnected():
                            connected = True
                            break
                        time.sleep(1)

                    if connected:
                        print("Network connected!")
                    else:
                        print("Connection failed!")

                elif setting == 2:
                    print("1.0, running on ESP32")
                elif setting == 3:
                    print("Setting things up...")
                    with open("connection", "w") as f:
                        ...
                    
                    print("You detach mpremote once you press enter")
                    input()

                    mpremote_connection()
                    
    else:
        if inp.replace(" ", "") != "" and inp.replace(" ", "") != "exit":
            print("Invalid command")