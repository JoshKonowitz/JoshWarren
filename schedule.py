from datetime import datetime
from itertools import combinations, product
import pandas as pd

def convert_time(string):
    time = datetime.strptime(string, '%H:%M').time()
    return time

#defines a course and sets variables based on inputs
class Course:
    def __init__(self, name, professor, times, lab):
        self.subject = name[:3]
        self.number = name[-3:]
        self.professor = professor
        self.days = [day for day in times]
        self.times = times
        self.lab = lab
        for x in self.times:
            for b in range(len(self.times[x])):
                self.times[x][b] = convert_time(self.times[x][b])

class Lab:
    def __init__(self, name, professor, times):
        self.subject = name[:3]
        self.number = name[-3:]
        self.professor = professor
        self.days = [day for day in times]
        self.times = times
        for x in self.times:
            for b in range(len(self.times[x])):
                self.times[x][b] = convert_time(self.times[x][b])

#checks if two courses' days and times overlap
def check_overlap(a, b):
    for x,y in product(a.days, b.days):
        if x == y:
            if b.times[x][0] < a.times[x][0]:
                a, b = b, a
            if a.times[x][1] > b.times[x][0]:
                return True
    else:
        return False

#checks if course is already in schedule
def check_repeat(a, b):
    return a.subject + a.number == b.subject + b.number

#checks if course is before user's earliest time
def check_early(a, early_time):
    for day in a.times:
        if a.times[day][0] < convert_time(early_time):
            return True

#checks if course if after user's lastest time
def check_late(a, late_time):
    for day in a.times:
        if a.times[day][0]  > convert_time(late_time):
            return True

#if the user does not want courses on friday, checks if course is on friday
def check_friday(a, friday_option):
    if friday_option:
        return "F" in a.days

#checks if the course's duration in minutes is longer than user's max class duration time
def check_duration(a, max_duration):
    if max_duration != None:
        for day in a.times:
            duration = (a.times[day][1].hour - a.times[day][0].hour)*60 + a.times[day][1].minute - a.times[day][0].minute + (a.times[day][1].second - a.times[day][0].second)/60.0
            if duration > max_duration:
                return True

def check_lab(option):
    labs_needed = []
    for a in option:
        if a.lab == True:
            for b in labs:
                for c in option:
                    if check_overlap(b, c):
                        return False, option
            else:
                labs_needed.append(b)
    else:
        if len(labs_needed) > 0:
            new_options = labs_needed
            for x in option:
                new_options.append(x)
            option = tuple(new_options)
        return True, option

def run_checks(a, b, early_time, late_time, friday_option, max_duration):
    checks = [
        check_overlap(a,b),
        check_repeat(a, b),
        check_early(a, early_time),
        check_late(a, late_time),
        check_friday(a, friday_option),
        check_duration(a, max_duration)
    ]
    if True in checks:
        return True

#prints schedule in txt format
def print_schedule(option):
    for x in range(2):
        print("="*24)
    for week_day in ["M", "T", "W", "R", "F"]:
        schedule = []
        for course in option:
            for day in course.days:
                if day == week_day:
                    schedule.append([str(course.subject + course.number + " " + str(course.times[day][0]) + "-" + str(course.times[day][1])), course.times[day][0]])
        schedule.sort(key=lambda x: x[1])
        if len(schedule) > 0:
            print("___________"+week_day+"____________")
        for course in schedule:
            print(course[0])

classes = [
    Course("MAR357", "", {"T": ["17:00", "18:20"], "R": ["17:00", "18:20"]}, False),
    Course("MAR444", "", {"T": ["12:30", "13:50"], "R": ["12:30", "13:50"]}, False),
    Course("MAR444", "", {"T": ["15:30", "16:50"], "R": ["15:30", "16:50"]}, False),
    Course("ACC252", "", {"T": ["11:00", "12:20"], "R": ["11:00", "12:20"]}, False),
    Course("ACC252", "", {"T": ["12:30", "13:50"], "R": ["12:30", "13:50"]}, False),
    Course("IST345", "", {"W": ["17:15", "20:05"]}, False),
    Course("IST345", "", {"T": ["9:30", "10:50"], "R": ["9:30", "10:50"]}, False),
    Course("IST345", "", {"T": ["17:15", "20:05"]}, False),
    Course("IST421", "", {"T": ["9:30", "12:15"]}, False),
    Course("IST421", "", {"W": ["9:30", "12:15"]}, False),
    Course("IST421", "", {"R": ["14:00", "16:45"]}, False),

]
labs = [

]

#user preferences
early_time = "9:30"
number_of_classes = 5
late_time = "19:00"
friday_option = True
max_duration = 500

#runs all possible combinations of courses based on user request number
all_options = list(combinations(classes, number_of_classes))

new_options = []
for option in all_options:
    for a, b in product(option, option):
        if a != b:
            if run_checks(a, b, early_time, late_time, friday_option, max_duration):
                break
    else:
        new_options.append(option)
final_options = []
for option in new_options:
    check, new_option = check_lab(option)
    if check:
        final_options.append(new_option)

for x in final_options:
    print_schedule(x)