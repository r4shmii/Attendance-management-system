import csv
import config


def mark_attendance(date, records):
    rows_to_add = []
    for roll_no, status in records.items():
        rows_to_add.append([date, roll_no, status])

    with open(config.ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows_to_add)

    return True, f"Attendance marked for {date}"


def get_attendance_by_date(date):
    with open(config.ATTENDANCE_FILE, "r") as f:
        reader = csv.DictReader(f)
        return [row for row in reader if row["date"] == date]
