class Course:
    def __init__(self, crscode, crsName):
        self.crscode = crscode
        self.crsName = crsName
        self.sections = []  # section objects

    def add_section(self, sec):
        self.sections.append(sec)

    def get_section(self, secnum):
        for section in self.sections:
            if section.section_number == secnum:
                return section
        return -1

    def get_sections(self, secs):
        lst = []
        for i in secs:
            n = self.get_section(i)
            if n != -1:
                print(f"Section {i} found. remaining seats: {n.remainingSeats}")
                lst.append(n)
            else:
                print(f"Section {i} not found.")
        return lst
