import os
import configparser_custom
config = configparser_custom.ConfigParser()

def custom_eval(stuff:str):
    return eval(stuff, {}, {})

literal_eval = custom_eval
filename = "grades.ini"

def init_diary() -> None:
    try:
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                pass
    except:
        try:
            with open(filename, "r"):
                pass
        except OSError:
            with open(filename, "w") as f:
                f.write("")

def backup_grades():
    f = open(filename, "r")
    file = f.readlines()
    f.close()

    with open("grades_backup.ini", "w") as f:
        for i in file:
            f.write(i)
        f.close()

def write_grade(subject:str="", grades:list[float]=None) -> None: # type: ignore
    if grades is None:
        grades = []

    if subject == "" or not grades: return
    
    config_file = config.read(filename)
    
    backup_grades()
    
    if not subject in config:
        config.add_section(subject)
        config[subject]["grades"] = str(grades)
        print(config[subject]["grades"])
    else:
        currgrades = read_grades(subject)
        for i in grades:
            currgrades.append(float(i))

        config[subject]["grades"] = str(currgrades)
    
    with open(filename, 'w') as configfile:
        config.write(configfile)

def read_grades(subject:str="") -> list[float]:
    try:
        config_file = config.read(filename)
        return literal_eval(config[subject]["grades"]) # pyright: ignore[reportReturnType]
    except:
        return []

def get_all_grades() -> list[dict]:
    grades = []
    config_file = config.read(filename)
    for i in config.sections():
        grades.append({"subject": i, "grades": literal_eval(config[i]["grades"])})

    return grades

def is_valid_grade(subject:str="") -> bool:
    is_valid = False
    config_file = config.read(filename)
    try:
        config[subject]["grades"]
        is_valid = True
    except: # we return EARLY because at this point we know it doesn't exist, therfore there is nothing more to do
        is_valid = False
        return is_valid
    
    # if it does somehow exist, check if we have ANY grades inside of it
    grades = config[subject]["grades"]
    
    if len(grades) == 0:
        is_valid = False

    return is_valid


