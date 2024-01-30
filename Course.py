from Section import Section


class Course:
    def __init__(self, crscode, crsName):
        self.crscode = crscode
        self.crsName = crsName
        self.sections = []  # section objects

    def add_section(self, sec):
        self.sections.append(sec)

    def get_section(self, secnum):
        sec = []
        section: Section
        for section in self.sections:
            if secnum in section.section_number:
                sec += [section]

        return sec

    def getsec(self, secnum):
        section: Section
        for section in self.sections:
            if section.section_number == secnum:
                return section

        return -1

    def get_sections(self, secs):
        lst = []
        for i in secs:
            searched = self.get_section(i)
            if searched:
                section: Section
                for section in searched:
                    lst.append(section)
        return lst
