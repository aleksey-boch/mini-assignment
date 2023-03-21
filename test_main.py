from datetime import datetime
from unittest import TestCase

from main import Bookings, BookingEntity, Itinerary


class TestItinerary(TestCase):
    def test_equal_negative(self):
        a = Itinerary('LHR', 'AMS')
        b = Itinerary('GVA', 'AMS')
        self.assertFalse(a == b)

    def test_equal(self):
        a = Itinerary('LHR', 'AMS')
        b = Itinerary('LHR', 'AMS')
        self.assertTrue(a == b)


class TestBookingEntity(TestCase):
    def test_add_itinerary(self):
        bruce = BookingEntity(
            pax_name='Bruce',
            departure=datetime(2020, 6, 4, 11, 4),
            itineraries=[Itinerary('GVA', 'AMS')],
        )
        bruce.add_itinerary(Itinerary('AMS', 'LHR'))

        self.assertEqual(len(bruce.itineraries), 2)


class TestBookings(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bookings = Bookings()

    def _get_alice_booking(self) -> BookingEntity:
        return BookingEntity(
            pax_name='Alice',
            departure=datetime(2020, 5, 26, 6, 45),
            itineraries=[Itinerary('LHR', 'AMS')],
        )

    def _get_bruce_booking(self) -> BookingEntity:
        bruce = BookingEntity(
            pax_name='Bruce',
            departure=datetime(2020, 6, 4, 11, 4),
            itineraries=[Itinerary('GVA', 'AMS')],
        )
        bruce.add_itinerary(Itinerary('AMS', 'LHR'))
        return bruce

    def _get_cindy_booking(self) -> BookingEntity:
        cindy = BookingEntity(
            pax_name='Cindy',
            departure=datetime(2020, 6, 6, 10, 0),
            itineraries=[Itinerary('AAL', 'AMS'), Itinerary('AMS', 'LHR')],
        )
        cindy.add_itinerary([Itinerary('LHR', 'JFK'), Itinerary('JFK', 'SFO')])

        return cindy

    def test_append(self):
        alice = self._get_alice_booking()
        self.bookings.append(alice)
        self.assertEqual(len(self.bookings), 1)

    def test_extend(self):
        alice = self._get_alice_booking()
        bruce = self._get_bruce_booking()
        self.bookings.extend((alice, bruce))
        self.assertEqual(len(self.bookings), 2)

    def test_select_itinerary_before_date(self):
        alice = self._get_alice_booking()
        bruce = self._get_bruce_booking()
        cindy = self._get_cindy_booking()
        self.bookings.extend((alice, bruce, cindy))

        data = self.bookings.select_itinerary_before_date(dt=datetime(2020, 6, 6, 9, 0))
        names = [t.pax_name for t in data]
        self.assertEqual(names, ['Alice', 'Bruce'])

    def test_select_itinerary(self):
        alice = self._get_alice_booking()
        bruce = self._get_bruce_booking()
        cindy = self._get_cindy_booking()
        derek = BookingEntity(
            pax_name='Derek',
            departure=datetime(2020, 6, 12, 8, 9),
            itineraries=[Itinerary('AMS', 'LHR')],
        )

        erica = BookingEntity(
            pax_name='Erica',
            departure=datetime(2020, 6, 13, 20, 40),
            itineraries=[Itinerary('ATL', 'AMS'), Itinerary('AMS', 'AAL')],
        )

        fred = BookingEntity(
            pax_name='Fred',
            departure=datetime(2020, 6, 14, 9, 10),
            itineraries=[Itinerary('AMS', 'CDG'), Itinerary('CDG', 'LHR')],
        )

        self.bookings.extend((alice, bruce, cindy, derek, erica, fred))

        data = self.bookings.select_itinerary(Itinerary('AMS', 'LHR'))
        names = [t.pax_name for t in data]
        self.assertEqual(names, ['Bruce', 'Cindy', 'Derek'])
