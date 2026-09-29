# Attendance Management System

A simple desktop attendance management system built in Python using Tkinter.
This project was made as part of a course assignment to apply basic programming
concepts like file handling, functions, GUI design, and modular code organization.

## Overview

The system lets a teacher (or admin) add students, mark their daily attendance,
and check attendance reports, all from a simple window-based app. All data is
stored in CSV files, so no database setup is needed to run it.

## Features

- Add new students with roll number, name and class
- View the list of all registered students
- Mark daily attendance (present/absent) for every student
- View attendance records for a specific date
- Generate an attendance percentage report for all students
- List students whose attendance is below 75%

## Technologies Used

- Python 3
- Tkinter (built-in) for the desktop GUI
- Built-in `csv` module for data storage
- Built-in `datetime` module for date validation

## Project Structure

```
attendance_management_system/
├── main.py                 # entry point, opens the GUI window
├── student_manager.py      # add/view students (logic only)
├── attendance_manager.py   # mark and view attendance (logic only)
├── report_generator.py     # attendance percentage reports (logic only)
├── utils.py                # helper functions (file setup, date check)
├── config.py                # file paths and constants
└── data/
    ├── students.csv
    └── attendance.csv
```

## How to Install and Run

1. Make sure Python 3 is installed on your system.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run the program:

```
python main.py
```

5. A window will open with buttons for each feature.

Note: Tkinter comes pre-installed with Python on Windows and macOS. On some
Linux distributions you may need to install it separately with:
```
sudo apt-get install python3-tk
```

## How to Test

- Open the app and add 2-3 students using "Add Student".
- Mark attendance for today's date using "Mark Attendance".
- Try marking attendance for another date so there is more than one record.
- Use "View Attendance Report" to see percentages and "Low Attendance List"
  to see students below 75%.
- Try entering an invalid date format to check that the validation works.

## Notes

- All data is saved automatically inside the `data` folder as CSV files, so
  your records stay even after closing the app.
- This is a beginner-level project with a simple GUI, built without any
  external libraries beyond Python's standard library.
