from datetime import datetime

class Task:
    def __init__(self, title, start_time, end_time, priority=0):
        self.title = title
        self.start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M") if isinstance(start_time, str) else start_time
        self.end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M") if isinstance(end_time, str) else end_time
        self.priority = int(priority)

    def to_dict(self):
        return {
            "title": self.title,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M"),
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M"),
            "priority": self.priority
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["start_time"], data["end_time"], data["priority"])
