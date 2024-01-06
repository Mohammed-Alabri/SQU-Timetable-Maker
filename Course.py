class Course:
    def __init__(self, crscode, crsName):
        self.crscode = crscode
        self.crsName = crsName
        self.sections = []  # section objects

    def add_section(self, sec):
        self.sections.append(sec)

    def get_section(self, secnum):
        sec = []
        for section in self.sections:
            if secnum in section.section_number:
                sec += [section]

        return sec

    def getsec(self, secnum):
        for section in self.sections:
            if section.section_number == secnum:
                return section

        return -1

    def get_sections(self, secs):
        lst = []
        for i in secs:
            n = self.get_section(i)
            if n:
                for t in n:
                    print(f"Section {t.section_number} found. remaining seats: {t.remainingSeats}")
                    lst.append(t)
            else:
                print(f"Section {i} not found.")
        return lst
