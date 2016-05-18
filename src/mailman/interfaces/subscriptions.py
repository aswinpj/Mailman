# Copyright (C) 2009-2016 by the Free Software Foundation, Inc.
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

"""Membership interface for REST."""

from collections import namedtuple
from enum import Enum
from mailman.interfaces.errors import MailmanError
from mailman.interfaces.member import DeliveryMode, MembershipError
from zope.interface import Interface


@public
class MissingUserError(MailmanError):
    """A an invalid user id was given."""

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    def __str__(self):
        return self.user_id


@public
class SubscriptionPendingError(MailmanError):
    def __init__(self, mlist, email):
        super().__init__()
        self.mlist = mlist
        self.email = email


@public
class TooManyMembersError(MembershipError):
    def __init__(self, subscriber, list_id, role):
        super().__init__()
        self.subscriber = subscriber
        self.list_id = list_id
        self.role = role


_RequestRecord = namedtuple(
    'RequestRecord',
    'email display_name delivery_mode, language')


@public
def RequestRecord(email, display_name='',
                  delivery_mode=DeliveryMode.regular,
                  language=None):
    if language is None:
        from mailman.core.constants import system_preferences
        language = system_preferences.preferred_language
    return _RequestRecord(email, display_name, delivery_mode, language)


@public
class TokenOwner(Enum):
    """Who 'owns' the token returned from the registrar?"""
    no_one = 0
    subscriber = 1
    moderator = 2


@public
class ISubscriptionService(Interface):
    """General Subscription services."""

    def get_members():
        """Return a sequence of all members of all mailing lists.

        The members are sorted first by fully-qualified mailing list name,
        then by subscribed email address, then by role.  Because the user may
        be a member of the list under multiple roles (e.g. as an owner and as
        a digest member), the member can appear multiple times in this list.
        Roles are sorted by: owner, moderator, member.

        :return: The list of all members.
        :rtype: list of `IMember`
        """

    def get_member(member_id):
        """Return a member record matching the member id.

        :param member_id: A member id.
        :type member_id: int
        :return: The matching member, or None if no matching member is found.
        :rtype: `IMember`
        """

    def find_members(subscriber=None, list_id=None, role=None):
        """Search for members matching some criteria.

        The members are sorted first by list-id, then by subscribed
        email address, then by role.  Because the user may be a member
        of the list under multiple roles (e.g. as an owner and as a
        digest member), the member can appear multiple times in this
        list.

        :param subscriber: The email address or user id of the user getting
            subscribed.  This argument may contain asterisks, which will be
            interpreted as wildcards in the search pattern.
        :type subscriber: string or int
        :param list_id: The list id of the mailing list to search for the
            subscriber's memberships on.
        :type list_id: string
        :param role: The member role.
        :type role: `MemberRole`
        :return: The list of all memberships, which may be empty.
        :rtype: list of `IMember`
        """

    def find_member(subscriber=None, list_id=None, role=None):
        """Search for a member matching some criteria.

        This is like find_members() but is guaranteed to return exactly
        one member.

        :param subscriber: The email address or user id of the user getting
            subscribed.
        :type subscriber: string or int
        :param list_id: The list id of the mailing list to search for the
            subscriber's memberships on.
        :type list_id: string
        :param role: The member role.
        :type role: `MemberRole`
        :return: The member matching the given criteria or None if no
            members match the criteria.
        :rtype: `IMember` or None
        :raises TooManyMembersError: when the given criteria matches
            more than one membership.
        """

    def __iter__():
        """See `get_members()`."""

    def leave(list_id, email):
        """Unsubscribe from a mailing list.

        :param list_id: The list id of the mailing list the user is
            unsubscribing from.
        :type list_id: string
        :param email: The email address of the user getting unsubscribed.
        :type email: string
        :raises InvalidEmailAddressError: if the email address is not valid.
        :raises NoSuchListError: if the named mailing list does not exist.
        :raises NotAMemberError: if the given address is not a member of the
            mailing list.
        """

    def unsubscribe_members(list_id, emails):
        """Unsubscribe a batch of members from a mailing list.

        :param list_id: The list id to operate on.
        :type list_id: string
        :param emails: A list of email addresses of the members getting
            unsubscribed.  Only list members with a role of `member` can be
            unsubscribed via this interface.
        :type emails: list of strings
        :return: A two item tuple whose first item is a set of all the
            successfully unsubscribed email addresses and second item is
            a set of all unsuccessful email addresses.
        :rtype: 2-tuple of (set-of-strings, set-of-strings)
        :raises NoSuchListError: if the named mailing list does not exist.
        """
