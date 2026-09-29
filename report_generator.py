import csv
import config
import student_manager


def get_report():
    students = student_manager.get_all_students()

    with open(config.ATTENDANCE_FILE, "r") as f:
        reader = csv.DictReader(f)
        attendance_rows = list(reader)

    report = []
    for student in students:
        roll_no = student["roll_no"]
        student_records = [r for r in attendance_rows if r["roll_no"] == roll_no]
        total = len(student_records)
        present = len([r for r in student_records if r["status"] == "present"])

        if total == 0:
            percentage = 0
        else:
            percentage = round((present / total) * 100, 2)

        report.append({
            "roll_no": roll_no,
            "name": student["name"],
            "present": present,
            "total": total,
            "percentage": percentage
        })

    return report


def get_low_attendance():
    full_report = get_report()
    return [r for r in full_report if r["total"] > 0 and r["percentage"] < config.LOW_ATTENDANCE_LIMIT]
