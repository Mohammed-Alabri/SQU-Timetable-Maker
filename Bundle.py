# class to group all courses objects
class Bundle:
    def __init__(self, courses):
        self.courses = courses

    def find_course(self, crscode):
        for course in self.courses:
            if course.crscode == crscode:
                return course
        return -1

    def names(self):
        lst = []
        for i in self.courses:
            lst.append(i.crscode)
        return lst

    def find_by_coll(self, code):
        lst = []
        for course in self.courses:
            if course.crscode[:4] == code:
                lst.append(course)
        return Bundle(lst)

    def get_sections(self, crscode, sections=None):
        course = self.find_course(crscode)
        if course != -1:
            if sections is None:
                return course.sections
            else:
                return course.get_sections(sections)
        else:
            return -1
