import datetime
import interactions


class Event:
    def __init__(self, id, date: datetime.datetime, name: str, channel: interactions.Channel, url: str):
        self.id = id
        self.members = []
        self.datetime = date
        self.name = name
        self.channel = channel
        self.url = url
