import math
import numpy as np
import curses

class Course:
    def __init__(self, course_id, name, credits):
        self.course_id = course_id
        self.name = name
        self.credits = credits

class Student:
    def __init__(self, student_id, name, dob):
        self.student_id = student_id
        self.name = name
        self.dob = dob
        self.marks = {}  
        self.gpa = 0.0

    def add_mark(self, course_id, mark):
        self.marks[course_id] = math.floor(mark * 10) / 10.0

    def calculate_gpa(self, courses_dict):
        if not self.marks:
            self.gpa = 0.0
            return self.gpa

        marks_list = []
        credits_list = []

        for cid, mark in self.marks.items():
            if cid in courses_dict:
                marks_list.append(mark)
                credits_list.append(courses_dict[cid].credits)

        if not credits_list or sum(credits_list) == 0:
            self.gpa = 0.0
        else:
            marks_arr = np.array(marks_list)
            credits_arr = np.array(credits_list)
            raw_gpa = np.average(marks_arr, weights=credits_arr)
            self.gpa = math.floor(raw_gpa * 10) / 10.0

        return self.gpa


def safe_addstr(stdscr, y, x, text, attr=0):
    """Hàm ghi chuỗi an toàn chống crash tràn màn hình Windows"""
    max_y, max_x = stdscr.getmaxyx()
    if y < max_y and x < max_x:
        try:
            stdscr.addstr(y, x, text[: max_x - x - 1], attr)
        except curses.error:
            pass


def get_input(stdscr, prompt, y, x):
    """Hàm nhập liệu ổn định trên Windows Terminal"""
    safe_addstr(stdscr, y, x, prompt)
    stdscr.refresh()
    curses.echo()
    try:
        user_input = stdscr.getstr(y, x + len(prompt)).decode('utf-8').strip()
    except Exception:
        user_input = ""
    curses.noecho()
    return user_input


def main(stdscr):
    curses.curs_set(1)
    stdscr.clear()

    students = []
    courses = {}

    while True:
        try:
            val = get_input(stdscr, "Enter number of students: ", 0, 0)
            num_students = int(val)
            if num_students > 0:
                break
        except ValueError:
            pass

    for i in range(num_students):
        stdscr.clear()
        safe_addstr(stdscr, 0, 0, f"=== Student {i+1}/{num_students} ===", curses.A_BOLD)
        sid = get_input(stdscr, "ID: ", 1, 0)
        name = get_input(stdscr, "Name: ", 2, 0)
        dob = get_input(stdscr, "DoB (DD/MM/YYYY): ", 3, 0)
        students.append(Student(sid, name, dob))

    stdscr.clear()
    while True:
        try:
            val = get_input(stdscr, "Enter number of courses: ", 0, 0)
            num_courses = int(val)
            if num_courses > 0:
                break
        except ValueError:
            pass

    for i in range(num_courses):
        stdscr.clear()
        safe_addstr(stdscr, 0, 0, f"=== Course {i+1}/{num_courses} ===", curses.A_BOLD)
        cid = get_input(stdscr, "ID: ", 1, 0)
        cname = get_input(stdscr, "Name: ", 2, 0)
        
        while True:
            try:
                cred = int(get_input(stdscr, "Credits: ", 3, 0))
                break
            except ValueError:
                pass
        courses[cid] = Course(cid, cname, cred)

    for cid, course in courses.items():
        stdscr.clear()
        safe_addstr(stdscr, 0, 0, f"=== Marks for Course: {course.name} ({cid}) ===", curses.A_BOLD)
        for idx, student in enumerate(students):
            while True:
                try:
                    mark_val = float(get_input(stdscr, f"Mark for {student.name} ({student.student_id}): ", idx + 1, 0))
                    student.add_mark(cid, mark_val)
                    break
                except ValueError:
                    pass

    for student in students:
        student.calculate_gpa(courses)

    students.sort(key=lambda s: s.gpa, reverse=True)

    stdscr.clear()
    curses.curs_set(0)
    
    safe_addstr(stdscr, 0, 0, "STUDENT GPA RANKING (DESCENDING)", curses.A_BOLD | curses.A_UNDERLINE)
    header = f"{'Rank':<5} | {'ID':<10} | {'Name':<20} | {'GPA':<5}"
    safe_addstr(stdscr, 2, 0, header, curses.A_REVERSE)
    safe_addstr(stdscr, 3, 0, "-" * len(header))

    for idx, student in enumerate(students):
        row_str = f"{idx+1:<5} | {student.student_id:<10} | {student.name:<20} | {student.gpa:<5.1f}"
        safe_addstr(stdscr, 4 + idx, 0, row_str)

    safe_addstr(stdscr, 6 + len(students), 0, "Press ANY key to exit...", curses.A_DIM)
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)