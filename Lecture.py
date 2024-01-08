class Lecture:
    def __init__(self, section: str, time: str, location: str):
        self.section = section
        self.time = time[4:]
        self.day = time[:3]
        self.location = location
