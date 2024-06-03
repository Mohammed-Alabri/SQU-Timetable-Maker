import copy

import requests as rq
import json
from Course import Course
from Section import Section
from Bundle import Bundle
from Lecture import Lecture


def extract_data():
    global r
    attempts = 0
    print("Getting courses data...")
    while attempts < 5:
        try:
            url = "https://portal.squ.edu.om/web/guest/master-timetable?p_p_id" \
                  "=mastertimetable_WAR_prjMasterTimetable_INSTANCE_xIkL1MpZID2p&p_p_lifecycle=2&p_p_state=normal" \
                  "&p_p_mode=view&p_p_resource_id=getMasterTimetable&p_p_cacheability=cacheLevelPage&p_p_col_id" \
                  "=column-1&p_p_col_count=1&ramadan_time=No"
            r = rq.get(url)
            break
        except Exception as e:
            print(f"ERROR: {e}")
            attempts += 1

    result = json.loads(r.text)
    return result


def extract_seating_data():
    global n
    attempts = 0
    print("Getting seating data...")
    while attempts < 5:
        try:
            url = "https://portal.squ.edu.om/web/guest/sectioncounts?p_p_id" \
                  "=sectioncount_WAR_prjSectionCount_INSTANCE_MBwsbhYD3YWj&p_p_lifecycle=2&p_p_state=normal&p_p_mode" \
                  "=view&p_p_resource_id=getAllCourseInfo&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1" \
                  "&p_p_col_count=1"
            n = rq.get(url)
            break
        except Exception as e:
            print(f"ERROR: {e}")
            attempts += 1

    result = json.loads(n.text)
    return result


# rearrange courses using classes(Course and Section)
def class_rearrange_courses() -> Bundle:
    data = extract_data()
    courses = Bundle()
    last_section = ''
    # seat = extract_seating_data()
    l1 = None
    l2 = None
    l3 = None
    for course in data:
        fcor = courses.find_course(course['crscode'])
        if fcor == -1:  # not found course
            cor = Course(course['crscode'], course['crsName'])
            sec = Section(cor, str(course['sectno']),
                          Lecture(str(course['sectno']), course['timeBldRoom'], course['building']),
                          course['instructor'],
                          course['exam_date_time'])
            cor.add_section(sec)
            courses.add_course(cor)
            last_section = sec
            l1 = None
            l2 = None
            l3 = None
        else:  # found course
            sec = fcor.getsec(str(course['sectno']))

            if sec != -1:  # found section
                sec.add_lecture(Lecture(str(course['sectno']), course['timeBldRoom'], course['building']))
                sec.add_instructors(course['instructor'])
            elif sec == -1 and last_section.section_number == str(course['sectno'] - 1) and l1 == None:  # lab section
                sec = Section(fcor, last_section.section_number + '-' + str(course['sectno']),
                              copy.copy(last_section.lectures), copy.copy(last_section.instructors),
                              last_section.exam_date_time)
                sec.add_lecture(Lecture(str(course['sectno']), course['timeBldRoom'], course['building']))
                sec.add_instructors(course['instructor'])
                # print(sec.section_number, sec.course.crscode, last_section.section_number, last_section.course.crscode)
                fcor.sections.remove(last_section)
                fcor.add_section(sec)
                l1 = sec
            elif sec == -1 and last_section.section_number == str(course['sectno'] - 1):
                sec = l1
                sec.add_lecture(Lecture(str(course['sectno']), course['timeBldRoom'], course['building']))
                sec.add_instructors(course['instructor'])
            elif sec == -1 and last_section.section_number == str(course['sectno'] - 2) and l2 == None:  # lab section
                sec = Section(fcor, last_section.section_number + '-' + str(course['sectno']),
                              copy.copy(last_section.lectures), copy.copy(last_section.instructors),
                              last_section.exam_date_time)
                sec.add_lecture(Lecture(str(course['sectno']), course['timeBldRoom'], course['building']))
                sec.add_instructors(course['instructor'])
                fcor.add_section(sec)
                l2 = sec
            elif sec == -1 and last_section.section_number == str(course['sectno'] - 2):
                sec = l2
                sec.add_lecture(Lecture(str(course['sectno']), course['timeBldRoom'], course['building']))
                sec.add_instructors(course['instructor'])
            elif sec == -1 and last_section.section_number == str(course['sectno'] - 3) and l3 == None:  # lab section
                sec = Section(fcor, last_section.section_number + '-' + str(course['sectno']),
                              copy.copy(last_section.lectures), copy.copy(last_section.instructors),
                              last_section.exam_date_time)
                sec.add_lecture(Lecture(str(course['sectno']), course['timeBldRoom'], course['building']))
                sec.section_number += '-' + sec.section_number[:-1] + '3'
                sec.add_instructors(course['instructor'])
                fcor.add_section(sec)
                l3 = sec
            elif sec == -1 and last_section.section_number == str(course['sectno'] - 3):
                sec = l3
                sec.add_lecture(Lecture(str(course['sectno']), course['timeBldRoom'], course['building']))
                sec.add_instructors(course['instructor'])
            else:  # not found section
                sec = Section(cor, str(course['sectno']),
                              Lecture(str(course['sectno']), course['timeBldRoom'], course['building']),
                              course['instructor'],
                              course['exam_date_time'])
                fcor.add_section(sec)
                last_section = sec
                l1 = None
                l2 = None
                l3 = None
            # sec.set_seating(get_seating(seat, sec.course.crscode, str(course['sectno'])))
    return courses


def find_course(crscode, lst):
    for course in lst:
        if course.crscode == crscode:
            return course
    return -1


def get_seating(data, crscode, section):
    for crs in data:
        if crs['crscode'] == crscode and str(crs['sectno']) == section:
            return dict(list(crs.items())[6:])

    return -1
