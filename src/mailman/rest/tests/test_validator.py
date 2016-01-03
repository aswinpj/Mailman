# Copyright (C) 2015-2016 by the Free Software Foundation, Inc.
#
# This file is part of GNU Mailman.
#
# GNU Mailman is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# GNU Mailman is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# GNU Mailman.  If not, see <http://www.gnu.org/licenses/>.

"""Test REST validators."""

__all__ = [
    'TestValidators',
    ]


import unittest

from mailman.interfaces.usermanager import IUserManager
from mailman.rest.validator import (
    list_of_strings_validator, subscriber_validator)
from mailman.testing.layers import RESTLayer
from zope.component import getUtility



class TestValidators(unittest.TestCase):
    layer = RESTLayer

    def test_list_of_strings_validator_single(self):
        # This validator should turn a single key into a list of keys.
        self.assertEqual(list_of_strings_validator('ant'), ['ant'])

    def test_list_of_strings_validator_multiple(self):
        # This validator should turn a single key into a list of keys.
        self.assertEqual(
            list_of_strings_validator(['ant', 'bee', 'cat']),
            ['ant', 'bee', 'cat'])

    def test_list_of_strings_validator_invalid(self):
        # Strings are required.
        self.assertRaises(ValueError, list_of_strings_validator, 7)
        self.assertRaises(ValueError, list_of_strings_validator, ['ant', 7])

    def test_subscriber_validator_int_uuid(self):
        # Convert from an existing user id to a UUID.
        anne = getUtility(IUserManager).make_user('anne@example.com')
        uuid = subscriber_validator('3.0')(str(anne.user_id.int))
        self.assertEqual(anne.user_id, uuid)

    def test_subscriber_validator_hex_uuid(self):
        # Convert from an existing user id to a UUID.
        anne = getUtility(IUserManager).make_user('anne@example.com')
        uuid = subscriber_validator('3.1')(anne.user_id.hex)
        self.assertEqual(anne.user_id, uuid)

    def test_subscriber_validator_no_int_uuid(self):
        # API 3.1 does not accept ints as subscriber id's.
        anne = getUtility(IUserManager).make_user('anne@example.com')
        self.assertRaises(ValueError,
                          subscriber_validator('3.1'), str(anne.user_id.int))

    def test_subscriber_validator_bad_int_uuid(self):
        # In API 3.0, UUIDs are ints.
        self.assertRaises(ValueError,
                          subscriber_validator('3.0'), 'not-a-thing')

    def test_subscriber_validator_bad_int_hex(self):
        # In API 3.1, UUIDs are hexes.
        self.assertRaises(ValueError,
                          subscriber_validator('3.1'), 'not-a-thing')

    def test_subscriber_validator_email_address_API30(self):
        self.assertEqual(subscriber_validator('3.0')('anne@example.com'),
                         'anne@example.com')

    def test_subscriber_validator_email_address_API31(self):
        self.assertEqual(subscriber_validator('3.1')('anne@example.com'),
                         'anne@example.com')
