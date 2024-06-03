class Lecture:
    def __init__(self, section: str, time: str, location: str):
        self.section = section
        self.time = time[4:]
        self.start_time, self.end_time = self.time.split("-")
        self.day = time[:3]
        self.location = location
        self.tts = [int(self.start_time.replace(':', '')), int(self.end_time.replace(':', ''))]

