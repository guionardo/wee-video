import unittest

from src.services.stats_service import StatsService


class TestStatsService(unittest.TestCase):

    def test_series(self):
        stats = StatsService()
        stats.add_data(10_000, 2)    # 5000bps
        stats.add_data(25_000_000, 10)   # 2500000bps

        avg_time = stats.get_average_process_time(12000)
        self.assertLess(0.001, avg_time-0.00057)
