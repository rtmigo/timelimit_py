# SPDX-FileCopyrightText: (c) 2020 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT


import unittest
import time

from timelimited import timelimited_thread, LimitedTimeOutError


def fast():
    return 777


def slow():
    time.sleep(55)
    return 777


class TestRunInThread(unittest.TestCase):

    def test_no_timeout(self):
        self.assertEqual(timelimited_thread(fast, timeout=0.1, default=13),
                         777)  # успели получить результат

    def test_timeout_default(self):
        self.assertEqual(timelimited_thread(slow, timeout=0.1, default=13),
                         13)  # не успели

    def test_timeout_exception(self):
        with self.assertRaises(LimitedTimeOutError):
            timelimited_thread(slow, timeout=0.1)

    def test_no_args(self):
        def getSmiley():
            return ":)"

        self.assertEqual(timelimited_thread(getSmiley), ":)")

    def test_two_args(self):
        def getSmiley():
            return ":)"

        self.assertEqual(timelimited_thread(getSmiley), ":)")

        def concat(a, b):
            return a + b

        self.assertEqual(timelimited_thread(concat, args=("A", "B")), "AB")