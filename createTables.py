import copy
import itertools
from tabulate import tabulate

times = ['', '08:00-09:20', "08:00-09:50", "10:00-11:20", "10:00-11:50", "12:00-13:20",
         "12:00-13:50", "14:15-15:35", "14:15-16:05", "16:15-17:35", "16:15-18:05"]
table_layout = [['Days/ Times', 'SUN', 'MON', 'TUE', 'WED', 'THU'],
                ['08:00-09:20', '', '', '', '', ''],
                ["08:00-09:50", '', '', '', '', ''],
                ["10:00-11:20", '', '', '', '', ''],
                ["10:00-11:50", '', '', '', '', ''],
                ["12:00-13:20", '', '', '', '', ''],
                ["12:00-13:50", '', '', '', '', ''],
                ["14:15-15:35", '', '', '', '', ''],
                ["14:15-16:05", '', '', '', '', ''],
                ["16:15-17:35", '', '', '', '', ''],
                ["16:15-18:05", '', '', '', '', '']]


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
        for course in table:
            for i in course.times:
                taken.append(i[:6])
        if len(taken) == len(set(taken)):
            correct.append(table)
    return correct


def print_table(courses):
    tt = copy.deepcopy(table_layout)
    for section in courses:
        for n in section.times:
            day = n[:3]
            time = n[4:]
            tt[times.index(time)][tt[0].index(day)] = f"{section.course.crscode}/{section.section_number}"
    print(tabulate(rm_empty(tt), headers="firstrow", tablefmt="fancy_grid"))


def free_day_filter(day, tables_list):
    filtered = []

    def dd(day, table):
        for section in table:
            for i in section.times:
                if i[:3] == day:
                    return False
        return True

    for table in tables_list:
        if dd(day, table):
            filtered.append(table)
    return filtered


def free_time_filter(time, tables_list):
    filtered = []

    def tt(time, table):
        for section in table:
            for i in section.times:
                if i[4:6] == time:
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
