import os
import csv
from datetime import datetime
import config


def setup_files():
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(config.STUDENTS_FILE):
        with open(config.STUDENTS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(config.STUDENTS_HEADER)

    if not os.path.exists(config.ATTENDANCE_FILE):
        with open(config.ATTENDANCE_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(config.ATTENDANCE_HEADER)


def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False
