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
            origin='GVA',
            destination='AMS',
        )
        bruce.add_itinerary('LHR')

        self.assertEqual(2, len(bruce.layovers))

    def test_add_itineraries(self):
        bruce = BookingEntity(
            pax_name='Bruce',
            departure=datetime(2020, 6, 4, 11, 4),
            origin='GVA',
            destination='AMS',
        )
        bruce.add_itineraries(['LHR', 'JFK', 'SFO'])

        self.assertEqual(4, len(bruce.layovers))


class TestBookings(TestCase):
    def setUp(self):
        self.bookings = Bookings()

    def _get_alice_booking(self) -> BookingEntity:
        return BookingEntity(
            pax_name='Alice',
            departure=datetime(2020, 5, 26, 6, 45),
            origin='LHR',
            destination='AMS',
        )

    def _get_bruce_booking(self) -> BookingEntity:
        bruce = BookingEntity(
            pax_name='Bruce',
            departure=datetime(2020, 6, 4, 11, 4),
            origin='GVA',
            destination='AMS',
        )
        bruce.add_itinerary('LHR')
        return bruce

    def _get_cindy_booking(self) -> BookingEntity:
        cindy = BookingEntity(
            pax_name='Cindy',
            departure=datetime(2020, 6, 6, 10, 0),
            origin='AAL',
            destination='AMS',
        )
        cindy.add_itineraries(['LHR', 'JFK', 'SFO'])
        return cindy

    def test_append(self):
        alice = self._get_alice_booking()
        self.bookings.append(alice)
        self.assertEqual(1, len(self.bookings))

    def test_extend(self):
        alice = self._get_alice_booking()
        bruce = self._get_bruce_booking()
        self.bookings.extend((alice, bruce))
        self.assertEqual(2, len(self.bookings))

    def test_add_booking(self):
        self.bookings.add_booking(
            pax_name='Alice',
            departure=datetime(2020, 5, 26, 6, 45),
            origin='LHR',
            destination='AMS',
        )
        self.assertEqual(1, len(self.bookings))

    def test_select_before_date(self):
        alice = self._get_alice_booking()
        bruce = self._get_bruce_booking()
        cindy = self._get_cindy_booking()
        self.bookings.extend((alice, bruce, cindy))

        data = self.bookings.select_before_date(dt=datetime(2020, 6, 6, 9, 0))
        names = [t.pax_name for t in data]
        self.assertEqual(['Alice', 'Bruce'], names)

    def test_select_layover(self):
        alice = self._get_alice_booking()
        bruce = self._get_bruce_booking()
        cindy = self._get_cindy_booking()
        self.bookings.extend((alice, bruce, cindy))

        self.bookings.add_booking(
            pax_name='Derek',
            departure=datetime(2020, 6, 12, 8, 9),
            origin='AMS',
            destination='LHR',
        )

        erica = BookingEntity(
            pax_name='Erica',
            departure=datetime(2020, 6, 13, 20, 40),
            origin='ATL',
            destination='AMS',
        )
        erica.add_itinerary('AAL')

        fred = BookingEntity(
            pax_name='Fred',
            departure=datetime(2020, 6, 14, 9, 10),
            origin='AMS',
            destination='CDG',
        )
        fred.add_itinerary('LHR')
        self.bookings.extend((erica, fred))

        data = self.bookings.select_layover('AMS', 'LHR')
        names = [t.pax_name for t in data]
        self.assertEqual(['Bruce', 'Cindy', 'Derek'], names)
