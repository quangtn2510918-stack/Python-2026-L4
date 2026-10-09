import curses

def safe_addstr(stdscr, y, x, text, attr=0):
    max_y, max_x = stdscr.getmaxyx()
    if y < max_y and x < max_x:
        try:
            stdscr.addstr(y, x, text[: max_x - x - 1], attr)
        except curses.error:
            pass

def display_gpa_ranking(stdscr, students):
    stdscr.clear()
    curses.curs_set(0)
    
    safe_addstr(stdscr, 0, 0, "STUDENT GPA RANKING", curses.A_BOLD | curses.A_UNDERLINE)
    header = f"{'Rank':<5} | {'ID':<10} | {'Name':<20} | {'GPA':<5}"
    safe_addstr(stdscr, 2, 0, header, curses.A_REVERSE)
    safe_addstr(stdscr, 3, 0, "-" * len(header))

    for idx, student in enumerate(students):
        row_str = f"{idx+1:<5} | {student.student_id:<10} | {student.name:<20} | {student.gpa:<5.1f}"
        safe_addstr(stdscr, 4 + idx, 0, row_str)

    safe_addstr(stdscr, 6 + len(students), 0, "Press ANY key to exit.", curses.A_DIM)
    stdscr.refresh()
    stdscr.getch()