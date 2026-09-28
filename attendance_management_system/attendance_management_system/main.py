import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import utils
import student_manager
import attendance_manager
import report_generator

BG_COLOR = "#f0f4f8"
HEADER_COLOR = "#2c3e50"
ACCENT_COLOR = "#3498db"
TEXT_COLOR = "#2c3e50"
FONT_NORMAL = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 11, "bold")
FONT_HEADER = ("Segoe UI", 16, "bold")


def style_setup():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TButton", font=FONT_NORMAL, padding=8)
    style.map("TButton", background=[("active", ACCENT_COLOR)])

    style.configure("Accent.TButton", font=FONT_BOLD, padding=10,
                     background=ACCENT_COLOR, foreground="white")
    style.map("Accent.TButton", background=[("active", "#2980b9")])

    style.configure("Treeview", font=FONT_NORMAL, rowheight=26)
    style.configure("Treeview.Heading", font=FONT_BOLD)


def center_window(win, width, height):
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")


def make_toplevel(title, width, height):
    win = tk.Toplevel(root)
    win.title(title)
    win.configure(bg=BG_COLOR)
    win.resizable(False, False)
    center_window(win, width, height)
    return win


def add_student_window():
    win = make_toplevel("Add Student", 320, 260)

    tk.Label(win, text="Add New Student", font=FONT_HEADER, bg=BG_COLOR, fg=HEADER_COLOR).pack(pady=(15, 10))

    form = tk.Frame(win, bg=BG_COLOR)
    form.pack(padx=20)

    tk.Label(form, text="Roll No", font=FONT_NORMAL, bg=BG_COLOR, fg=TEXT_COLOR, anchor="w").grid(row=0, column=0, sticky="w", pady=6)
    roll_entry = ttk.Entry(form, width=22)
    roll_entry.grid(row=0, column=1, pady=6)

    tk.Label(form, text="Name", font=FONT_NORMAL, bg=BG_COLOR, fg=TEXT_COLOR, anchor="w").grid(row=1, column=0, sticky="w", pady=6)
    name_entry = ttk.Entry(form, width=22)
    name_entry.grid(row=1, column=1, pady=6)

    tk.Label(form, text="Class", font=FONT_NORMAL, bg=BG_COLOR, fg=TEXT_COLOR, anchor="w").grid(row=2, column=0, sticky="w", pady=6)
    class_entry = ttk.Entry(form, width=22)
    class_entry.grid(row=2, column=1, pady=6)

    def submit():
        success, msg = student_manager.add_student(
            roll_entry.get(), name_entry.get(), class_entry.get()
        )
        if success:
            messagebox.showinfo("Success", msg)
            win.destroy()
        else:
            messagebox.showerror("Error", msg)

    ttk.Button(win, text="Add Student", style="Accent.TButton", command=submit).pack(pady=20)


def view_students_window():
    win = make_toplevel("All Students", 420, 320)

    tk.Label(win, text="Registered Students", font=FONT_HEADER, bg=BG_COLOR, fg=HEADER_COLOR).pack(pady=(15, 10))

    tree_frame = tk.Frame(win, bg=BG_COLOR)
    tree_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    tree = ttk.Treeview(tree_frame, columns=("roll", "name", "class"), show="headings")
    tree.heading("roll", text="Roll No")
    tree.heading("name", text="Name")
    tree.heading("class", text="Class")
    tree.column("roll", width=80, anchor="center")
    tree.column("name", width=180)
    tree.column("class", width=100, anchor="center")
    tree.pack(fill="both", expand=True)

    students = student_manager.get_all_students()
    if not students:
        messagebox.showinfo("No students", "No students added yet.")

    for s in students:
        tree.insert("", "end", values=(s["roll_no"], s["name"], s["class"]))


def mark_attendance_window():
    students = student_manager.get_all_students()
    if not students:
        messagebox.showinfo("No students", "Add some students first.")
        return

    win = make_toplevel("Mark Attendance", 340, 480)

    tk.Label(win, text="Mark Attendance", font=FONT_HEADER, bg=BG_COLOR, fg=HEADER_COLOR).pack(pady=(15, 5))

    date_frame = tk.Frame(win, bg=BG_COLOR)
    date_frame.pack(pady=(0, 10))
    tk.Label(date_frame, text="Date (YYYY-MM-DD):", font=FONT_NORMAL, bg=BG_COLOR, fg=TEXT_COLOR).pack(side="left")
    date_entry = ttk.Entry(date_frame, width=14)
    date_entry.pack(side="left", padx=5)

    tk.Label(win, text="Untick a student to mark them absent", font=("Segoe UI", 9, "italic"), bg=BG_COLOR, fg="#7f8c8d").pack(pady=(0, 5))

    list_frame = tk.Frame(win, bg="white", bd=1, relief="solid")
    list_frame.pack(fill="both", expand=True, padx=20)

    check_vars = {}
    for s in students:
        var = tk.BooleanVar(value=True)
        chk = tk.Checkbutton(list_frame, text=f"{s['name']}  ({s['roll_no']})", variable=var,
                              font=FONT_NORMAL, bg="white", anchor="w", padx=10, pady=4)
        chk.pack(fill="x")
        check_vars[s["roll_no"]] = var

    def submit():
        date = date_entry.get().strip()
        if not utils.is_valid_date(date):
            messagebox.showerror("Error", "Enter date in YYYY-MM-DD format.")
            return

        records = {}
        for roll_no, var in check_vars.items():
            records[roll_no] = "present" if var.get() else "absent"

        success, msg = attendance_manager.mark_attendance(date, records)
        messagebox.showinfo("Done", msg)
        win.destroy()

    ttk.Button(win, text="Save Attendance", style="Accent.TButton", command=submit).pack(pady=15)


def view_attendance_window():
    date = simpledialog.askstring("Enter Date", "Date (YYYY-MM-DD):")
    if not date:
        return

    records = attendance_manager.get_attendance_by_date(date)

    win = make_toplevel(f"Attendance on {date}", 320, 340)

    tk.Label(win, text=f"Attendance - {date}", font=FONT_HEADER, bg=BG_COLOR, fg=HEADER_COLOR).pack(pady=(15, 10))

    tree_frame = tk.Frame(win, bg=BG_COLOR)
    tree_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    tree = ttk.Treeview(tree_frame, columns=("roll", "status"), show="headings")
    tree.heading("roll", text="Roll No")
    tree.heading("status", text="Status")
    tree.column("roll", width=100, anchor="center")
    tree.column("status", width=100, anchor="center")
    tree.pack(fill="both", expand=True)

    if not records:
        messagebox.showinfo("No data", "No attendance found for that date.")

    for r in records:
        tree.insert("", "end", values=(r["roll_no"], r["status"]))


def view_report_window():
    win = make_toplevel("Attendance Report", 480, 340)

    tk.Label(win, text="Attendance Report", font=FONT_HEADER, bg=BG_COLOR, fg=HEADER_COLOR).pack(pady=(15, 10))

    tree_frame = tk.Frame(win, bg=BG_COLOR)
    tree_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    columns = ("roll", "name", "present", "total", "percentage")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    tree.heading("roll", text="Roll No")
    tree.heading("name", text="Name")
    tree.heading("present", text="Present")
    tree.heading("total", text="Total")
    tree.heading("percentage", text="Percentage")
    tree.column("roll", width=70, anchor="center")
    tree.column("name", width=140)
    tree.column("present", width=70, anchor="center")
    tree.column("total", width=60, anchor="center")
    tree.column("percentage", width=90, anchor="center")
    tree.pack(fill="both", expand=True)

    report = report_generator.get_report()
    if not report:
        messagebox.showinfo("No data", "No students to report on.")

    for r in report:
        tree.insert("", "end", values=(r["roll_no"], r["name"], r["present"], r["total"], f"{r['percentage']}%"))


def view_low_attendance_window():
    win = make_toplevel("Low Attendance", 360, 300)

    tk.Label(win, text="Below 75% Attendance", font=FONT_HEADER, bg=BG_COLOR, fg="#c0392b").pack(pady=(15, 10))

    list_frame = tk.Frame(win, bg="white", bd=1, relief="solid")
    list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

    listbox = tk.Listbox(list_frame, font=FONT_NORMAL, bd=0, highlightthickness=0)
    listbox.pack(fill="both", expand=True, padx=5, pady=5)

    low_list = report_generator.get_low_attendance()
    if not low_list:
        listbox.insert("end", "Everyone is above the limit. Nice.")
    else:
        for r in low_list:
            listbox.insert("end", f"{r['name']} ({r['roll_no']}) - {r['percentage']}%")


is_fullscreen = False


def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)
    fullscreen_btn.config(text="Exit Fullscreen" if is_fullscreen else "Fullscreen")


def exit_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = False
    root.attributes("-fullscreen", False)
    fullscreen_btn.config(text="Fullscreen")


if __name__ == "__main__":
    utils.setup_files()

    root = tk.Tk()
    root.title("Attendance Management System")
    root.configure(bg=BG_COLOR)
    root.resizable(True, True)
    center_window(root, 360, 500)

    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Escape>", exit_fullscreen)

    style_setup()

    header = tk.Frame(root, bg=HEADER_COLOR, height=90)
    header.pack(fill="x")
    tk.Label(header, text="Attendance Manager", font=("Segoe UI", 18, "bold"),
              bg=HEADER_COLOR, fg="white").pack(pady=25)

    fullscreen_btn = tk.Button(header, text="Fullscreen", font=("Segoe UI", 8), command=toggle_fullscreen,
                                bg=HEADER_COLOR, fg="white", bd=0, activebackground="#1a252f",
                                activeforeground="white", cursor="hand2")
    fullscreen_btn.place(relx=1.0, x=-12, y=12, anchor="ne")

    main_area = tk.Frame(root, bg=BG_COLOR)
    main_area.pack(fill="both", expand=True)

    button_frame = tk.Frame(main_area, bg=BG_COLOR)
    button_frame.place(relx=0.5, rely=0.5, anchor="center")

    buttons = [
        ("Add Student", add_student_window),
        ("View All Students", view_students_window),
        ("Mark Attendance", mark_attendance_window),
        ("View Attendance by Date", view_attendance_window),
        ("View Attendance Report", view_report_window),
        ("Low Attendance List", view_low_attendance_window),
    ]

    for text, command in buttons:
        ttk.Button(button_frame, text=text, width=28, command=command).pack(fill="x", pady=6)

    ttk.Button(button_frame, text="Exit", width=28, command=root.destroy).pack(fill="x", pady=(20, 0))

    root.mainloop()
