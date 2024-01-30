import copy
import itertools
from Lecture import Lecture
from Section import Section

times = ['', '08:00-09:20', "08:00-09:50", "10:00-11:20", "10:00-11:50", "12:00-13:20",
         "12:00-13:50", "14:15-15:35", "14:15-16:05", "16:15-17:35", "16:15-18:05"]
table_layout = [['Days/ Times', 'SUN', 'MON', 'TUE', 'WED', 'THU'],
                ['08:00\n-09:20', '', '', '', '', ''],
                ["08:00\n-09:50", '', '', '', '', ''],
                ["10:00\n-11:20", '', '', '', '', ''],
                ["10:00\n-11:50", '', '', '', '', ''],
                ["12:00\n-13:20", '', '', '', '', ''],
                ["12:00\n-13:50", '', '', '', '', ''],
                ["14:15\n-15:35", '', '', '', '', ''],
                ["14:15\n-16:05", '', '', '', '', ''],
                ["16:15\n-17:35", '', '', '', '', ''],
                ["16:15\n-18:05", '', '', '', '', '']]


def rm_empty(table):
    # rows
    empty = [''] * 5
    for row in reversed(range(1, 11)):  # len of table is 11
        if table[row][1:] == empty:
            del table[row]
    return table


def all_combinations(lst):
    combinations = itertools.product(*lst)
    return combinations


def get_correct_tables(combs):
    correct = []
    for table in combs:
        taken = []
        section: Section
        for section in table:
            lecture: Lecture
            for lecture in section.lectures:
                taken.append(lecture.day + lecture.time[:2])
        if len(taken) == len(set(taken)):
            correct.append(table)
    return correct


def print_table(table):
    tt = copy.deepcopy(table_layout)
    section: Section
    for section in table:
        lecture: Lecture
        for lecture in section.lectures:
            tt[times.index(lecture.time)][tt[0].index(lecture.day)] = f"{section.course.crscode}/{lecture.section}\n{lecture.location}"
    return rm_empty(tt)


def free_day_filter(day, tables_list):
    filtered = []

    def dd(dayy, tablee):
        section: Section
        for section in tablee:
            lecture: Lecture
            for lecture in section.lectures:
                if lecture.day == dayy:
                    return False
        return True

    for table in tables_list:
        if dd(day, table):
            filtered.append(table)
    return filtered


def free_time_filter(time, tables_list):
    filtered = []

    def tt(timee, tablee):
        section: Section
        for section in tablee:
            lecture: Lecture
            for lecture in section.lectures:
                if lecture.time[:2] == timee:
                    return False
        return True

    for table in tables_list:
        if tt(time, table):
            filtered.append(table)
    return filtered


def filters(flts, tables_list):
    for fil in flts:
        if fil.upper() in ['SUN', 'MON', 'TUE', 'WED', 'THU']:
            tables_list = free_day_filter(fil, tables_list)
        elif fil in ['8', '08', '10', '12', '14', '16']:
            if fil == '8':
                fil = '08'
            tables_list = free_time_filter(fil, tables_list)
    return tables_list
