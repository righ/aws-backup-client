# coding: utf-8
from unittest import TestCase
from datetime import timedelta

from dateutil.relativedelta import relativedelta


class TestTypeDelta(TestCase):
    def _makeOne(self, *args, **kwargs):
        from ..parser import TypeDelta
        return TypeDelta(*args, **kwargs)

    def test_relativedelta(self):
        typedelta = self._makeOne(cls=relativedelta)
        self.assertEqual(
            typedelta('1years 2months -3days'),
            relativedelta(years=1, months=2, days=-3))

    def test_timedelta(self):
        typedelta = self._makeOne(cls=timedelta)
        self.assertEqual(
            typedelta('1days 2hours -3minutes'),
            timedelta(days=1, hours=2, minutes=-3))

    def test_timedelta_raising(self):
        typedelta = self._makeOne(cls=timedelta)
        with self.assertRaises(TypeError):
            typedelta('1years 2months -3days')
