class Lecture:
    def __init__(self, section: str, day: str, start_time: str, end_time: str, location: str):
        self.section = section
        self.start_time = start_time
        self.end_time = end_time
        self.time = start_time + '-' + end_time
        self.day = day
        self.location = location
        self.tts = [int(self.start_time.replace(':', '')), int(self.end_time.replace(':', ''))]
