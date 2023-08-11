class Section:
    def __init__(self, course, section_number, time, building, instructor, exam_date_time):
        self.course = course
        self.section_number = section_number
        self.instructors = [instructor]
        self.times = [time]
        self.buildings = [building]
        self.exam_date_time = exam_date_time
        self.seatTaken = ''
        self.remainingSeats = ''
        self.totalReserved = ''
        self.reservedSeats = ''
        self.sectMax = ''

    def set_seating(self, dic):
        self.seatTaken = dic['seatTaken']
        self.remainingSeats = dic['remainingSeats']
        self.totalReserved = dic['totalReserved']
        self.reservedSeats = dic['reservedSeats']
        self.sectMax = dic['sectMax']

    def add_instructors(self, instructor):
        if instructor not in self.instructors:
            self.instructors.append(instructor)

    def add_lecture(self, time, building):
        if time not in self.times:
            self.times.append(time)
            self.buildings.append(building)

    def get_building(self, time):
        return self.buildings[self.times.index(time)]

    def print_all(self):
        print(self.section_number)
        print(self.instructors)
        print(self.times)
        print(self.buildings)
        print(self.exam_date_time)
        return
