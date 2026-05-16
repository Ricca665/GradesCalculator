import zipfile
import os
curr_path = ""
files = []

def update_path() -> None:
    global curr_path, files
    curr_path = os.getcwd()
    files = os.listdir(curr_path)

print("ESP32 PACKAGER V1.0")
os.chdir(input("Insert esp32 location: "))
update_path()

try:
    if "main.py" not in files:
        raise FileNotFoundError("Unable to continue setup: no main file")
    
    for i in ["package.py", "connector_app.py", "__pycache__", "package.zip"]:
        file = i
        try:
            index = files.index(i)
        except ValueError:
            if i != "__pycache__" and i != "package.zip":
                print(f"WARNING: Unable to find file: {i}, skipping")
            continue
        files.pop(index)

    for i in files:
        if not os.path.exists(i):
            print(f"File {i} doesn't exist!")
            exit(1)

except Exception as e:
    print(f"An error has occured: {e}")
    exit(1)

print("Writing package file...")
with zipfile.ZipFile('package.zip', 'w') as zip:
    for i in files:
        zip.write(i)

print("Done!")

