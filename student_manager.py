import csv
import config


def student_exists(roll_no):
    with open(config.STUDENTS_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["roll_no"] == roll_no:
                return True
    return False


def add_student(roll_no, name, student_class):
    roll_no = roll_no.strip()
    name = name.strip()
    student_class = student_class.strip()

    if roll_no == "" or name == "":
        return False, "Roll number and name can't be empty."

    if student_exists(roll_no):
        return False, "A student with this roll number already exists."

    with open(config.STUDENTS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([roll_no, name, student_class])

    return True, f"Student {name} added successfully."


def get_all_students():
    with open(config.STUDENTS_FILE, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)
