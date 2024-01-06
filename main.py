import copy
import msvcrt
import functions
import createTables
from time import sleep


def remove_wrong(secs):
    lst = []
    for sec in secs:
        if sec.isdigit() and sec not in lst and len(sec) > 1:
            lst.append(sec)
    return lst


def slow(num, courses, sections):
    print("Enter course code ex:COMP2102")
    for i in range(num):
        sub = input(f"{i + 1}: ").upper()
        course = courses.find_course(sub)
        while course == -1:
            print("Course code not found Please Try Again")
            sub = input(f"{i + 1}: ")
            course = courses.find_course(sub)
        for sec in course.sections:
            print(
                f"section {sec.section_number}, instructors: {str(sec.instructors)[1:-1]}, remainingSeats: {sec.remainingSeats}")
        secs = remove_wrong(input("Enter sections seberated by space: ").split())
        while len(secs) == 0:
            print("Please enter valid sections.")
            secs = remove_wrong(input("Enter sections seberated by space: ").split())
        sections.append(course.get_sections(secs))


def fast(num, courses, sections):
    print("Enter course code with wanted sections seperated by space ex:MATH2107 10 20 30 40...")
    for i in range(num):
        sub = input(f"{i + 1}: ").split()
        sub[0] = sub[0].upper()
        while courses.find_course(sub[0]) == -1:
            print("Course code not found Please Try Again")
            sub = input(f"{i + 1}: ").split()
            sub[0] = sub[0].upper()
        if len(sub) == 1:
            sections.append(courses.find_course(sub[0]).sections)
        else:
            sections.append(courses.get_sections(sub[0], remove_wrong(sub[1:])))


def main():
    print('welcome to SQU table maker. Made by: Mohammed Al-Abri.')
    print("Github: https://github.com/Mohammed-Alabri")
    courses = functions.class_rearrange_courses()
    num = input("Enter number of courses: ")
    while not num.isdigit() or int(num) < 2:
        print("Please Enter number bigger than 1")
        num = input("Enter number of courses: ")
    num = int(num)
    route = input("Please Enter type of route fast or slow: ")
    sections = []
    if route.lower() in ["fast", 'f']:
        fast(num, courses, sections)
    elif route.lower() in ['slow', 's']:
        slow(num, courses, sections)
    else:
        print("please try again")
        exit(0)

    combs = createTables.all_combinations(sections)
    combs = createTables.get_correct_tables(combs)
    print("Orginazing tables...")
    sleep(0.8)

    if len(combs) == 0:
        print("There no possible table, Please try again...")
    else:
        filtered = copy.deepcopy(combs)
        filters = []
        while True:
            if len(filtered) > 0:
                for i in filtered:
                    createTables.print_table(i)
            else:
                print("There no possible table, Please check free filters")
            print(f"Applied free filters: {str(filters)[1:-1]}")
            inn = input("Enter add or remove for free filters or else to exit: ")
            inn = inn.split()
            if inn[0].lower() in ['add', 'remove']:
                if inn[0] == "add":
                    filters.append(inn[1].upper())
                elif inn[0] == "remove":
                    if inn[1].upper() in filters:
                        filters.remove(inn[1].upper())
            else:
                break
            filtered = createTables.filters(filters, combs)

    print(f"Press any key to exit...")
    msvcrt.getch()


main()
