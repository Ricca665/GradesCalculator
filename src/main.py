import grades_utils
import diary_utils
import os
import sys
from number_utils import is_valid_number

features = True
inp = ""
oginput = input

try:
    import numpy as np
    import matplotlib.pyplot as plt
    from time import gmtime, strftime
except (ModuleNotFoundError, AttributeError):
    print("NOT ALL MODULES FOUND, FEATURES MIGHT BE LIMITED")
    try:
        from ulab import numpy as np # type: ignore
    except (ModuleNotFoundError, AttributeError):
        import numpy as np
    features = False

def input(str="") -> str:
    try:
        return oginput(str)
    except (KeyboardInterrupt, EOFError):
        print("\nexiting...")
        sys.exit()

folder_name = "grades_report"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

diary_utils.init_diary()

while inp != "exit":
    inp = input("[grades]> ").lower()

    if features:
        match inp:
            case "help":
                print("help: display this help guide")
                print("calculate grade (cg): yknow")
                print("check mininum grade (cmg): yknow")
                print("write to diary (wd): yknow")

            case "calculate grade" | "cg":
                grades = grades_utils.input_grades(add_list_option=True)
                print(f"Grade: {grades_utils.grades_calculator(grades):.2f}")

            case "check mininum grade" | "cmg":
                grades = grades_utils.input_grades(add_list_option=True)
                minimum_grade_to_fail = None
                
                for i in np.arange(10, -0.25, -0.25):
                    temp_grades = grades.copy()
                    temp_grades.append(i)    
                    grade = grades_utils.grades_calculator(temp_grades)

                    #print(grade)
                    if (grade < 6):
                        minimum_grade_to_fail = i
                        break
                
                if (minimum_grade_to_fail != None):
                    print("Minimun grade to fail: ", minimum_grade_to_fail)
                else:
                    print("No grade can make you fail ig lmao")
            case "write to diary" | "wd":
                diary_utils.write_grade(input("Insert subject name: ").lower(), grades_utils.input_grades())
            case "display grades" | "dg":
                if not features:
                    print("Feature disabled")
                    continue
                
                grade = grades_utils.input_grades(True)

                if len(grade) == 0 or len(grade) == 1:
                    continue

                saved_path = os.getcwd()

                os.chdir(folder_name)
                temp_folder_name = f"Grades {strftime("%Y-%m-%d", gmtime())}" # pyright: ignore[reportPossiblyUnboundVariable]
                if not os.path.exists(temp_folder_name):
                    os.makedirs(temp_folder_name)

                os.chdir(temp_folder_name)

                fig, ax = plt.subplots() # pyright: ignore[reportPossiblyUnboundVariable]
                x_axis = [x + 1 for x in range(len(grade))]
                y_axis = grade.copy()
                ax.plot(x_axis, y_axis)

                ax.set_xlabel("Time")
                ax.set_ylabel("Grade(s)")

                ax.set_title(f"Academic Progress Over time")
                
                plt.savefig(f"Grades {strftime("%Y-%m-%d %H_%M_%S", gmtime())}.png")# pyright: ignore[reportPossiblyUnboundVariable]
                plt.savefig(f"Grades {strftime("%Y-%m-%d %H_%M_%S", gmtime())}.pdf")# pyright: ignore[reportPossiblyUnboundVariable]
                os.chdir(saved_path)
                plt.show()# pyright: ignore[reportPossiblyUnboundVariable]

            case "archive all" | "aa":
                if not features:
                    print("Feature disabled")
                    continue

                grades = diary_utils.get_all_grades().copy()
                for i in grades:
                    subject = i["subject"]
                    grades = i["grades"]

                    saved_path = os.getcwd()
                    if len(grades) < 2:
                        print(f"Skipping plotting {subject}, reason: only one grade/zero grades found")
                        continue

                    os.chdir(folder_name)
                    temp_folder_name = f"Grades {strftime("%Y-%m-%d", gmtime())}" # pyright: ignore[reportPossiblyUnboundVariable]
                    if not os.path.exists(temp_folder_name):
                        os.makedirs(temp_folder_name)

                    os.chdir(temp_folder_name)

                    temp_folder_name = f"Grades {strftime("%Y-%m-%d", gmtime())} - {subject}" # pyright: ignore[reportPossiblyUnboundVariable]
                    if not os.path.exists(temp_folder_name):
                        os.makedirs(temp_folder_name)

                    os.chdir(temp_folder_name)


                    fig, ax = plt.subplots() # pyright: ignore[reportPossiblyUnboundVariable]
                    x_axis = [x + 1 for x in range(len(grades))]
                    y_axis = grades.copy()
                    ax.plot(x_axis, y_axis)

                    ax.set_xlabel("Time")
                    ax.set_ylabel("Grade(s)")

                    ax.set_title(f"Academic Progress Over time")
                    
                    plt.savefig(f"Grades {strftime("%Y-%m-%d %H_%M_%S", gmtime())} - {subject}.png") # pyright: ignore[reportPossiblyUnboundVariable]
                    plt.savefig(f"Grades {strftime("%Y-%m-%d %H_%M_%S", gmtime())} - {subject}.pdf") # pyright: ignore[reportPossiblyUnboundVariable]
                    os.chdir(saved_path)
                    #plt.show()

            case _:
                if inp.replace(" ", "") != "" and inp.replace(" ", "") != "exit":
                    print("Invalid command")
