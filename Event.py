import datetime


class Event:
    def __init__(self, id, date: datetime.datetime, name: str):
        self.id = id
        self.members = []
        self.datetime = date
        self.name = name
