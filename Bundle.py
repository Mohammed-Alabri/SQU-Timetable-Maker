from Course import Course


# class to group all courses objects
class Bundle:
    def __init__(self):
        self.courses = {}

    def add_course(self, course: Course):
        self.courses[course.crscode] = course

    def find_course(self, crscode):
        if crscode in self.courses:
            return self.courses[crscode]
        return None

    def names(self):
        lst = []
        for i in self.courses:
            lst.append(i.crscode)
        return lst

    def get_sections(self, crscode, sections=None):
        course: Course
        course = self.find_course(crscode)
        if course:
            if sections is None:
                return course.sections
            return course.get_sections(sections)
        raise RuntimeError("Course not found")
