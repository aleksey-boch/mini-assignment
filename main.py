from dataclasses import dataclass
from datetime import datetime


@dataclass
class Itinerary:
    """The entity of the itinerary"""
    origin: str
    destination: str

    def __eq__(self, other):
        return all((
            self.origin == other.origin,
            self.destination == other.destination,
        ))


@dataclass(init=False)
class BookingEntity:
    """The entity of the booking data structure"""

    pax_name: str = None
    departure_at: datetime = None
    itinerary: Itinerary = None  # A shortened itinerary - only the start and end points
    layovers: list[Itinerary] = None  # Full itinerary with all layovers

    def __init__(self, pax_name: str, departure: datetime, origin: str, destination: str) -> None:
        self.pax_name = pax_name
        self.departure_at = departure
        self.itinerary = Itinerary(origin, destination)
        self.layovers = [self.itinerary]

    def add_itinerary(self, destination: str) -> None:
        """Add one itinerary

        :param destination: destination airport
        """
        new_layover = Itinerary(self.itinerary.destination, destination)
        self.layovers.append(new_layover)
        self.itinerary = Itinerary(self.itinerary.origin, destination)

    def add_itineraries(self, destinations: list) -> int:
        """Add list of the itineraries

        :param destinations: List of the destination airports
        :return: Number of inserted items
        """
        for dest in destinations:
            self.add_itinerary(destination=dest)
        return len(destinations)

    def has_layover(self, origin: str, destination: str) -> bool:
        """Is bookings has two airports sequentially?

        :param origin: Origin airport
        :param destination: destination airport
        :return:
        """
        itinerary = Itinerary(origin, destination)
        for layover in self.layovers:
            if layover == itinerary:
                return True
        return False


class Bookings(list[BookingEntity]):
    """A data structure to manage bookings at an airline"""

    def add_booking(self, pax_name: str, departure: datetime, origin: str, destination: str) -> None:
        """Add one booking to the list

        :param pax_name: Passenger name
        :param departure: Departure date
        :param origin: Origin airport
        :param destination: destination airport
        """
        booking = BookingEntity(
            pax_name=pax_name,
            departure=departure,
            origin=origin,
            destination=destination,
        )
        super().append(booking)

    def select_before_date(self, dt: datetime):
        """Select bookings departing before a given time

        :param dt: A given time
        :return: List of bookings
        """
        return (booking for booking in self if booking.departure_at < dt)

    def select_layover(self, origin: str, destination: str):
        """Select bookings visiting two airports sequentially.

        :param origin: Origin airport
        :param destination: destination airport
        :return: List of bookings
        """
        return (booking for booking in self if booking.has_layover(origin, destination))
