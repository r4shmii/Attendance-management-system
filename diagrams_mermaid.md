# Design Diagrams - Attendance Management System

All diagrams below are written in Mermaid, so they render directly on GitHub.

---

## 1. System Architecture Diagram

The GUI never touches the CSV files directly. It goes through the manager modules, which use the shared utilities and config.

```mermaid
flowchart TD
    A["Presentation Layer<br/>main.py - Tkinter GUI"] --> B["student_manager.py"]
    A --> C["attendance_manager.py"]
    A --> D["report_generator.py"]
    B --> E["Utility Layer<br/>utils.py + config.py"]
    C --> E
    D --> E
    E --> F[("Data Storage Layer<br/>students.csv + attendance.csv")]
```

---

## 2. Process Flow / Workflow Diagram

```mermaid
flowchart TD
    S([Launch main.py]) --> M[Main menu window opens]
    M --> P{User picks an action}
    P --> A1[Add Student]
    P --> A2[View Students]
    P --> A3[Mark Attendance]
    P --> A4[View by Date]
    P --> A5[View Report]
    P --> A6[Low Attendance List]
    A1 --> V[Input is validated]
    A2 --> V
    A3 --> V
    A4 --> V
    A5 --> V
    A6 --> V
    V --> Q{Valid input?}
    Q -- No --> E[Show error message]
    E --> M
    Q -- Yes --> R[Read or write CSV file]
    R --> O[Result shown in window]
    O --> M
```

---

## 3. Use Case Diagram

```mermaid
flowchart LR
    T(["Teacher / Admin"])

    subgraph SYS["Attendance Management System"]
        U1([Add Student])
        U2([View All Students])
        U3([Mark Attendance])
        U4([View Attendance by Date])
        U5([View Attendance Report])
        U6([View Low Attendance List])
        U7([Validate Date Input])
    end

    T --- U1
    T --- U2
    T --- U3
    T --- U4
    T --- U5
    T --- U6
    U3 -. include .-> U7
    U4 -. include .-> U7
```

---

## 4. Class / Component Diagram

The project uses functions instead of full classes, so each box below is one Python module and the functions it provides.

```mermaid
classDiagram
    class main {
        +add_student_window()
        +view_students_window()
        +mark_attendance_window()
        +view_attendance_window()
        +view_report_window()
        +view_low_attendance_window()
        +toggle_fullscreen()
    }
    class student_manager {
        +student_exists()
        +add_student()
        +get_all_students()
    }
    class attendance_manager {
        +mark_attendance()
        +get_attendance_by_date()
    }
    class report_generator {
        +get_report()
        +get_low_attendance()
    }
    class utils {
        +setup_files()
        +is_valid_date()
    }
    class config {
        STUDENTS_FILE
        ATTENDANCE_FILE
        LOW_ATTENDANCE_LIMIT
    }

    main --> student_manager
    main --> attendance_manager
    main --> report_generator
    main --> utils
    report_generator --> student_manager
    student_manager --> config
    attendance_manager --> config
    report_generator --> config
    utils --> config
```

---

## 5. Sequence Diagram - Mark Attendance

```mermaid
sequenceDiagram
    actor T as Teacher
    participant G as main.py GUI
    participant U as utils
    participant A as attendance_manager
    participant C as attendance.csv

    T->>G: Click Mark Attendance
    G-->>T: Show checklist of students
    T->>G: Enter date, tick present students, click Save
    G->>U: is_valid_date(date)
    U-->>G: True
    G->>A: mark_attendance(date, records)
    A->>C: Write rows
    C-->>A: Write successful
    A-->>G: Return success and message
    G-->>T: Show confirmation popup
```

---

## 6. ER Diagram (CSV Storage)

The two CSV files behave like two related tables.

```mermaid
erDiagram
    STUDENTS ||--o{ ATTENDANCE : has
    STUDENTS {
        string roll_no PK
        string name
        string class
    }
    ATTENDANCE {
        string date
        string roll_no FK
        string status
    }
```
