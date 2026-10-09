import math
import numpy as np

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