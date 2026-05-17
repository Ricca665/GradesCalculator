import grades_utils
import diary_utils
import sys
import time
import configparser_custom
from ulab import numpy as np # type: ignore
config = configparser_custom.ConfigParser()

# constants
BOARD_NAME = "ESP32"
PYTHON_VER = sys.version
NETWORK_INI_NAME = "network.ini"

def check_connection() -> bool:
    connected = False

    for _ in range(20):
        if sta_if.isconnected():
            connected = True
            break
        time.sleep(1)

    return connected

def connection_message(connected:bool) -> None:
    if connected:
        print("Network connected!")
    else:
        print("Connection failed!")

try:
    import network # type: ignore
    print("Initializing networking...")
    sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
    try:
        with open(NETWORK_INI_NAME, "r") as f:
            pass
        
        config_file = config.read(NETWORK_INI_NAME)

        try:
            if "NETWORK" in config:
                print("Found connection configuration!")
                SSID = config["NETWORK"]["SSID"]
                PASSWORD = config["NETWORK"]["PASSWD"]
                print("Connecting...")
                sta_if.connect(SSID, PASSWORD)
                connected = check_connection()
                connection_message(connected)
            else:
                print("No network configuration found!")
        except:
            print("Invalid network configuration! Erasing...")
            with open(NETWORK_INI_NAME, "w") as f:
                pass
    except:
        print("No network configuration found!")
except:
    print("no esp32?")
    exit()

inp = ""
oginput = input

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

while inp != "exit":
    inp = input("[grades]> ").lower()
    if inp == "help":
        print("help: display this help guide")
        print("calculate grade (cg): yknow")
        print("check mininum grade (cmg): yknow")
        print("write to diary (wd): yknow")
        print("settings: yknow")

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
            print("No grade can make you fail ig")

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
                    ssid:bytes = b""
                    for i in sta_if.scan():
                        ssid,_,_,_,_,_ = i
                        networks.append(ssid.decode("utf-8", errors="replace"))
                    
                    print("Choose network to connect to:")

                    for index, ssid in enumerate(networks):
                        print(index, ssid)
                    
                    print("Select network to connect to")
                    network_choose = ""

                    while not network_choose.isdigit():
                        network_choose = input().lower()
                    
                    network_choose = int(network_choose)
                    if network_choose < 0 or network_choose >= len(networks):
                        print("invalid network!")
                        continue

                    password = input("Insert password for network: ")
                    print("Connecting...")
                    SSID = networks[network_choose]
                    sta_if.connect(SSID, password)
                    time.sleep(3)

                    connected = check_connection()
                    connection_message(connected)
                    config_file = config.read(NETWORK_INI_NAME)

                    if not "NETWORK" in config:
                        config.add_section("NETWORK")

                    config["NETWORK"]["SSID"] = SSID
                    config["NETWORK"]["PASSWD"] = password
                        
                    with open(NETWORK_INI_NAME, 'w') as configfile:
                        config.write(configfile)

                elif setting == 2:
                    print(f"1.0, running on {BOARD_NAME}")
                    print(f"Where python version is: {PYTHON_VER}")

                elif setting == 3:
                    print("Setting things up...")
                    with open("connection", "w") as f:
                        pass
                    
                    print("You detach mpremote once you press enter")
                    input()

                    mpremote_connection()
                    
    else:
        if inp.replace(" ", "") != "" and inp.replace(" ", "") != "exit":
            print("Invalid command")
