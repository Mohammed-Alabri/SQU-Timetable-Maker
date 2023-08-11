import requests as rq
import json
from Course import Course
from Section import Section
from Bundle import Bundle


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
def class_rearrange_courses():
    data = extract_data()
    courses = []
    seat = extract_seating_data()
    for course in data:
        fcor = find_course(course['crscode'], courses)
        sec = ''
        if fcor == -1:  # not found course
            cor = Course(course['crscode'], course['crsName'])
            sec = Section(cor, course['sectno'], course['timeBldRoom'], course['building'], course['instructor'],
                          course['exam_date_time'])
            cor.add_section(sec)
            courses.append(cor)
        else:  # found course
            sec = fcor.get_section(course['sectno'])
            if sec != -1:  # found section
                sec.add_lecture(course['timeBldRoom'], course['building'])
                sec.add_instructors(course['instructor'])
            elif sec == -1 and fcor.get_section(course['sectno'] - 1) != -1:  # lab section
                sec = fcor.get_section(course['sectno'] - 1)
                sec.add_lecture(course['timeBldRoom'], course['building'])
                sec.add_instructors(course['instructor'])
            else:  # not found section
                sec = Section(fcor, course['sectno'], course['timeBldRoom'], course['building'], course['instructor'],
                              course['exam_date_time'])
                fcor.add_section(sec)
            sec.set_seating(get_seating(seat, sec.course.crscode, sec.section_number))
    return Bundle(courses)


def find_course(crscode, lst):
    for course in lst:
        if course.crscode == crscode:
            return course
    return -1


def get_seating(data, crscode, section):
    for crs in data:
        if crs['crscode'] == crscode and crs['sectno'] == section:
            return dict(list(crs.items())[6:])

    return -1
