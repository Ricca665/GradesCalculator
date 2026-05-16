import diary_utils

def is_valid_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False

def grades_calculator(grades: list[float]) -> float:
    if not grades:
        return 0.0
    grade = 0
    length = len(grades)

    for i in grades:
        grade += float(i)

    return grade / length


def input_grades(add_list_option=False) -> list[float]:
    list_grades = []
    grade = None
    grab_from_list = False
    inp = ""

    if add_list_option:
        print("Insert type: ")
        print("1. Get grade from grades.ini")
        print("2. Add new grades from scratch")
        while inp != "1" and inp != "2":
            inp = input().lower()
        if inp == "1":
            grab_from_list = True

    if not grab_from_list:
        print("Insert grades, insert done when finished")
        while grade != "done":
            grade = input().lower()
            if (grade == "done"):
                continue

            if (is_valid_number(grade)):
                number = float(grade)
            else:
                print("Invalid grade")
                continue

            if (number > 10 or number < 0):
                print("Invalid grade")
                continue

            list_grades.append(float(grade))

        return list_grades
    else:
        grades = []

        subject = input("Insert subject: ").lower()

        if not diary_utils.is_valid_grade(subject):
            print("No grades for this subject")
            return []

        grades = diary_utils.read_grades(subject)
        return grades
