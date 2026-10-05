from __future__ import annotations

import unittest

from scripts.hardware_realtime.simulate_l4_microburst import estimate


class MicroburstModelTests(unittest.TestCase):
    def test_longer_window_models_reduction_and_wait(self):
        result = estimate(1.0, 100.0, 50.0)
        self.assertEqual(100, result["direct_wakeups"])
        self.assertEqual(20, result["batched_wakeups"])
        self.assertEqual(-80.0, result["estimated_wakeup_change_percent"])
        self.assertEqual(50.0, result["maximum_batch_wait_ms"])

    def test_shorter_window_reports_increase(self):
        result = estimate(1.0, 100.0, 5.0)
        self.assertEqual(200, result["batched_wakeups"])
        self.assertEqual(100.0, result["estimated_wakeup_change_percent"])

    def test_invalid_input_is_rejected(self):
        for arguments in ((0, 100, 10), (1, 0, 10), (1, 100, 0)):
            with self.subTest(arguments=arguments):
                with self.assertRaises(ValueError):
                    estimate(*arguments)


if __name__ == "__main__":
    unittest.main()
