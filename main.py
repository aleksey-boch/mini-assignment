from dataclasses import dataclass
from datetime import datetime
from typing import Union


@dataclass
class Itinerary:
    origin: str
    destination: str

    def __eq__(self, other):
        return all((
            self.origin == other.origin,
            self.destination == other.destination,
        ))


@dataclass
class BookingEntity:
    pax_name: str
    departure: datetime
    itineraries: list[Itinerary]

    def add_itinerary(self, itineraries: Union[Itinerary, list[Itinerary]]):
        if isinstance(itineraries, Itinerary):
            itineraries = [itineraries]

        self.itineraries.extend(itineraries)


class Bookings(list[BookingEntity]):
    def append(self, booking: BookingEntity) -> None:
        super().append(booking)

    def select_itinerary_before_date(self, dt: datetime):
        return list([x for x in self if x.departure < dt])

    def select_itinerary(self, itinerary: Itinerary):
        return list([x for x in self for y in x.itineraries if y == itinerary])


def main():
    pass


if __name__ == "__main__":
    main()
