from Lecture import Lecture


class Section:
    def __init__(self, course, section_number: str, lecture: Lecture, instructor: str):
        self.course = course
        self.section_number = section_number
        self.instructors = []
        if instructor.__class__ == list:
            self.instructors = instructor
        else:
            self.instructors.append(instructor)
        self.lectures = []
        if lecture.__class__ == list:
            self.lectures += lecture
        else:
            self.lectures.append(lecture)
        self.seatTaken = ''
        self.remainingSeats = ''
        self.totalReserved = ''
        self.reservedSeats = ''
        self.sectMax = ''

    def set_seating(self, dic):
        self.remainingSeats = dic['remainingSeats']
        self.totalReserved = dic['totalReserved']
        self.reservedSeats = dic['reservedSeats']
        self.sectMax = dic['sectMax']

    def add_instructors(self, instructor):
        if instructor not in self.instructors:
            self.instructors.append(instructor)

    def add_lecture(self, lecture: Lecture):
        self.lectures.append(lecture)
