import unittest

from timelimit import limit_process, TimeLimitExceeded


def pickleable_getSmiley():
    return ":)"


def pickleable_concat(a, b):
    return a + b


def pickleable_fast():
    return 777


def pickleable_slow():
    import time
    time.sleep(55)  # 55 секунд!
    return 777


class TestProcess(unittest.TestCase):

    def test_no_args(self):
        self.assertEqual(limit_process(pickleable_getSmiley),
                         ":)")

    def test_two_args(self):
        self.assertEqual(
            limit_process(pickleable_concat, args=("A", "B")),
            "AB")

    def test_fast_no_timeout(self):
        self.assertEqual(
            limit_process(pickleable_fast, timeout=0.5,
                          default=13), 777)  # успели получить результат

    def test_timeout_default(self):
        self.assertEqual(
            limit_process(pickleable_slow, timeout=0.5,
                          default=13), 13)  # не успели

    def test_timeout_error(self):
        with self.assertRaises(TimeLimitExceeded):
            limit_process(pickleable_slow, timeout=0.5)
