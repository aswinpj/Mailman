# Copyright (C) 2007-2008 by the Free Software Foundation, Inc.
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

"""The emergency hold rule."""

__all__ = ['Emergency']
__metaclass__ = type


from zope.interface import implements

from Mailman.i18n import _
from Mailman.interfaces import IRule



class Emergency:
    """The emergency hold rule."""
    implements(IRule)

    name = 'emergency'
    description = _(
        """The mailing list is in emergency hold and this message was not
        pre-approved by the list administrator.
        """)
    record = True

    def check(self, mlist, msg, msgdata):
        """See `IRule`."""
        return mlist.emergency and not msgdata.get('moderator_approved')