# Copyright (C) 2007 by the Free Software Foundation, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
# USA.

"""Doctest harness for the CookHeaders handler."""

import os
import unittest

from Mailman.testing.base import make_docfile_suite


def test_suite():
    suite = unittest.TestSuite()
    for filename in ('ack-headers', 'cook-headers', 'subject-munging',
                     'reply-to'):
        path = os.path.join('..', 'docs', filename + '.txt')
        suite.addTest(make_docfile_suite(path))
    return suite
