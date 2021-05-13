# SPDX-FileCopyrightText: (c) 2020 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT


import unittest
import time

from timelimit import limit_thread, TimeLimitExceeded


def fast():
    return 777


def slow():
    time.sleep(55)
    return 777


def getSmiley():
    return ":)"


def concat(a, b):
    return a + b


class TestRunInThread(unittest.TestCase):

    def test_no_timeup(self):
        self.assertEqual(limit_thread(fast, timeout=0.1, default=13),
                         777)  # успели получить результат

    def test_timeup_default(self):
        self.assertEqual(limit_thread(slow, timeout=0.1, default=13),
                         13)  # не успели

    def test_timeup_exception(self):
        with self.assertRaises(TimeLimitExceeded):
            limit_thread(slow, timeout=0.1)

    def test_no_args_as_none(self):
        self.assertEqual(limit_thread(getSmiley, timeout=1), ":)", )

    def test_no_args_as_empty_list(self):
        self.assertEqual(limit_thread(getSmiley, args=[], timeout=1),
                         ":)")

    def test_two_args(self):
        self.assertEqual(limit_thread(concat, args=("A", "B"), timeout=1), "AB")

    def test_two_args_no_timelimit(self):
        self.assertEqual(limit_thread(concat, args=("A", "B")), "AB")

    def test_timeout_none_two_args(self):
        self.assertEqual(limit_thread(concat, args=("A", "B"), timeout=None),
                         "AB")

    def test_timeout_none_no_args_as_none(self):
        self.assertEqual(limit_thread(getSmiley, timeout=None),
                         ":)")

    def test_timeout_none_no_args_as_empty_list(self):
        self.assertEqual(limit_thread(getSmiley, timeout=None, args=[]),
                         ":)")
