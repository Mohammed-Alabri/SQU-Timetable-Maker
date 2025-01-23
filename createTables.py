import itertools
from Lecture import Lecture
from Section import Section

days_layout = ['Days/ Times', 'SUN', 'MON', 'TUE', 'WED', 'THU']


def all_combinations(lst):
    print(lst)
    combinations = itertools.product(*lst)
    return combinations


def noconfilect(dic: dict):
    day: list
    for day in dic:
        dic[day].sort(key=lambda x: x[0])
        for i in range(len(dic[day]) - 1):
            if dic[day][i][1] >= dic[day][i + 1][0]:
                return False

    return True


def get_correct_tables(combs):
    correct = []
    for table in combs:
        taken = {'SUN': [], 'MON': [], 'TUE': [], 'WED': [], 'THU': []}
        section: Section
        for section in table:
            lecture: Lecture
            seclecs = {}
            for lecture in section.lectures:
                # sometimes there is duplicate in lectures
                if lecture.day + lecture.time not in seclecs:
                    taken[lecture.day] += [lecture.tts]
                    seclecs[lecture.day + lecture.time] = 0

        if noconfilect(taken):
            correct.append(table)
    return correct


def print_table(table):
    aa = []
    dic = {}
    for section in table:
        for lecture in section.lectures:
            if lecture.time not in dic:
                t = [''] * 6
                t[0] = lecture.time.replace('-', '-\n')
                dic[lecture.time] = t
                aa.append(t)
            dic[lecture.time][
                days_layout.index(lecture.day)] = f"{section.course.crscode}/{lecture.section}\n{lecture.location}"
    aa.sort(key=lambda x: int(x[0].replace(':', '').replace('-\n', '')))
    aa = [days_layout] + aa
    return aa


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
