import curses
from output import safe_addstr
from domain.student import Student
from domain.course import Course

def get_input(stdscr, prompt, y, x):
    safe_addstr(stdscr, y, x, prompt)
    stdscr.refresh()
    curses.echo()
    try:
        user_input = stdscr.getstr(y, x + len(prompt)).decode('utf-8').strip()
    except Exception:
        user_input = ""
    curses.noecho()
    return user_input

def input_students(stdscr):
    students = []
    while True:
        try:
            val = get_input(stdscr, "Enter number of students in class: ", 0, 0)
            num_students = int(val)
            if num_students > 0:
                break
        except ValueError:
            pass

    for i in range(num_students):
        stdscr.clear()
        safe_addstr(stdscr, 0, 0, f"Enter information for student #{i+1}", curses.A_BOLD)
        sid = get_input(stdscr, "Student ID: ", 1, 0)
        name = get_input(stdscr, "Student Name: ", 2, 0)
        dob = get_input(stdscr, "Date of Birth: ", 3, 0)
        students.append(Student(sid, name, dob))
        
    return students

def input_courses(stdscr):
    courses = {}
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
        safe_addstr(stdscr, 0, 0, f"Enter information for course #{i+1}", curses.A_BOLD)
        cid = get_input(stdscr, "Course ID: ", 1, 0)
        cname = get_input(stdscr, "Course Name: ", 2, 0)
        
        while True:
            try:
                cred = int(get_input(stdscr, "Credits: ", 3, 0))
                break
            except ValueError:
                pass
        courses[cid] = Course(cid, cname, cred)
        
    return courses

def input_marks(stdscr, courses, students):
    for cid in courses.keys():
        stdscr.clear()
        safe_addstr(stdscr, 0, 0, f"Inputting marks for course {cid}", curses.A_BOLD)
        for idx, student in enumerate(students):
            while True:
                try:
                    mark_val = float(get_input(stdscr, f"Enter mark for Student {student.name} ({student.student_id}): ", idx + 1, 0))
                    student.add_mark(cid, mark_val)
                    break
                except ValueError:
                    pass