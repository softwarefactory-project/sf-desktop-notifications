#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Red Hat
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from unittest import TestCase

from SFDesktopNotifications.sf_desktop_notifications import flatten_dict
from SFDesktopNotifications.sf_desktop_notifications import Filter


class TestFlattenDict(TestCase):
    def _test_flatten(self, input, expected=None):
        if expected is None:
            expected = input
        self.assertEqual(flatten_dict(input),
                         expected)

    def test_idempotency(self):
        self._test_flatten({})
        self._test_flatten({'a': 1})
        self._test_flatten({'a': 1,
                            'b': 2})

    def test_depth_one(self):
        d = {'a': {'b': 1},
             'c': 2}
        expected_d = {'a.b': 1,
                      'c': 2}
        self._test_flatten(d, expected_d)
        d = {'a': {'b': 1},
             'c': {2: 3}}
        expected_d = {'a.b': 1,
                      'c.2': 3}
        self._test_flatten(d, expected_d)
        d = {'a': {'b': 1,
                   'd': 3,
                   'e': 4},
             'c': 2}
        expected_d = {'a.b': 1,
                      'a.d': 3,
                      'a.e': 4,
                      'c': 2}
        self._test_flatten(d, expected_d)

    def test_depth_multi(self):
        d = {'a': {'b': 1,
                   'd': {'e': 3,
                         'f': 4,
                         'g': {'h': 5,
                               'i': 6}
                         },
                   'h': 7,
                   'i': {'j': 8}
                   },
             'c': 2}
        expected_d = {'a.b': 1,
                      'a.d.e': 3,
                      'a.d.f': 4,
                      'a.d.g.h': 5,
                      'a.d.g.i': 6,
                      'a.h': 7,
                      'a.i.j': 8,
                      'c': 2}
        self._test_flatten(d, expected_d)


class TestFilter(TestCase):
    def test_check(self):
        f = Filter('my_topic', {'a': 'b'}, 'my_username')
        self.assertFalse(f.check('another_topic',
                                 {'a': 'b'}))
        self.assertFalse(f.check('my_topic',
                                 {'a': 'c'}))
        self.assertFalse(f.check('my_topic',
                                 {'d': 'b'}))
        self.assertTrue(f.check('my_topic',
                                {'a': 'b'}))
