from dataclasses import dataclass
import datetime


@dataclass
class Movie:
    id: str
    title: str
    date_published: datetime.date
    avg_rating: float
    total_votes: int

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.title