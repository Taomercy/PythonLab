#!/usr/bin/env python
# -*- coding:utf-8 -*-
from hwwuex_check.test_case.object import TestCase


def check(log_path, check_type, modes, start=None, end=None):
    tc = TestCase(log_path, check_type, modes=modes)
    response = tc.check(start=start, end=end)
    return response
