import curses
from input import input_students, input_courses, input_marks
from output import display_gpa_ranking

def main(stdscr):
    curses.curs_set(1)
    stdscr.clear()

    # Step 1: Input students and courses
    students = input_students(stdscr)
    courses = input_courses(stdscr)

    # Step 2: Input marks
    input_marks(stdscr, courses, students)

    # Step 3: Calculate GPA for each student
    for student in students:
        student.calculate_gpa(courses)

    # Step 4: Sort students by GPA descending
    students.sort(key=lambda s: s.gpa, reverse=True)

    # Step 5: Display rankings
    display_gpa_ranking(stdscr, students)

if __name__ == "__main__":
    curses.wrapper(main)