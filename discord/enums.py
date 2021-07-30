# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2015-present Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import types
from collections import namedtuple

__all__ = (
    'Enum',
    'ChannelType',
    'ComponentType',
    'ButtonColor',
    'ButtonStyle',
    'PermissionType',
    'InteractionCallbackType',
    'TimestampStyle',
    'MessageType',
    'VoiceRegion',
    'SpeakingState',
    'VerificationLevel',
    'ContentFilter',
    'Status',
    'DefaultAvatar',
    'RelationshipType',
    'AuditLogAction',
    'AuditLogActionCategory',
    'UserFlags',
    'ActivityType',
    'HypeSquadHouse',
    'NotificationLevel',
    'PremiumType',
    'UserContentFilter',
    'FriendFlags',
    'TeamMembershipState',
    'Theme',
    'WebhookType',
    'ExpireBehaviour',
    'ExpireBehavior',
    'StickerType',
)


def _create_value_cls(name):
    cls = namedtuple('_EnumValue_' + name, 'name value')
    cls.__repr__ = lambda self: '<%s.%s: %r>' % (name, self.name, self.value)
    cls.__str__ = lambda self: '%s.%s' % (name, self.name)
    return cls


def _is_descriptor(obj):
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')


class EnumMeta(type):
    def __new__(cls, name, bases, attrs):
        value_mapping = {}
        member_mapping = {}
        member_names = []

        value_cls = _create_value_cls(name)
        for key, value in list(attrs.items()):
            is_descriptor = _is_descriptor(value)
            if key[0] == '_' and not is_descriptor:
                continue

            # Special case classmethod to just pass through
            if isinstance(value, classmethod):
                continue

            if is_descriptor:
                setattr(value_cls, key, value)
                del attrs[key]
                continue

            try:
                new_value = value_mapping[value]
            except KeyError:
                new_value = value_cls(name=key, value=value)
                value_mapping[value] = new_value
                member_names.append(key)

            member_mapping[key] = new_value
            attrs[key] = new_value

        attrs['_enum_value_map_'] = value_mapping
        attrs['_enum_member_map_'] = member_mapping
        attrs['_enum_member_names_'] = member_names
        actual_cls = super().__new__(cls, name, bases, attrs)
        value_cls._actual_enum_cls_ = actual_cls
        return actual_cls

    def __iter__(cls):
        return (cls._enum_member_map_[name] for name in cls._enum_member_names_)

    def __reversed__(cls):
        return (cls._enum_member_map_[name] for name in reversed(cls._enum_member_names_))

    def __len__(cls):
        return len(cls._enum_member_names_)

    def __repr__(cls):
        return '<enum %r>' % cls.__name__

    @property
    def __members__(cls):
        return types.MappingProxyType(cls._enum_member_map_)

    def __call__(cls, value):
        try:
            return cls._enum_value_map_[value]
        except (KeyError, TypeError):
            raise ValueError("%r is not a valid %s" % (value, cls.__name__))

    def __getitem__(cls, key):
        return cls._enum_member_map_[key]

    def __setattr__(cls, name, value):
        raise TypeError('Enums are immutable.')

    def __delattr__(cls, attr):
        raise TypeError('Enums are immutable')

    def __instancecheck__(self, instance):
        # isinstance(x, Y)
        # -> __instancecheck__(Y, x)
        try:
            return instance._actual_enum_cls_ is self
        except AttributeError:
            return False


class Enum(metaclass=EnumMeta):
    @classmethod
    def try_value(cls, value):
        try:
            return cls._enum_value_map_[value]
        except (KeyError, TypeError):
            return value


class ChannelType(Enum):
    text           = 0
    private        = 1
    voice          = 2
    group          = 3
    category       = 4
    news           = 5
    store          = 6
    news_thread    = 10
    public_thread  = 11
    private_thread = 12
    stage_voice    = 13


    def __str__(self):
        return self.name

class PermissionType(Enum):
    member = 0
    role   = 1

    # i use :meth:`getattr` so `codacy` don't cry and *my own* code is as clean as possible.
    def __str__(self):
        return getattr(self, 'name')

    def __int__(self):
        return getattr(self, 'value')


class ComponentType(Enum):
    ActionRow = 1
    Button = 2
    SelectMenu = 3

    def __str__(self):
        return getattr(self, 'name')

    def __int__(self):
        return getattr(self, 'value')

    def __eq__(self, other):
        return int(self) == other or str(self) == other


class ButtonStyle(Enum):
    """
    :class:`ButtonStyle`
    Represents the Style for a :class:`discord.Button`

    .. note ::
        For more information about the Button-Styles, visit the `Discord-API Documentation <https://discord.com/developers/docs/interactions/message-components#buttons-button-styles>`_.

    """

    blurple     = 1
    Primary     = 1
    grey        = 2
    gray        = 2
    Secondary   = 2
    green       = 3
    Success     = 3
    red         = 4
    Danger      = 4
    url         = 5
    link        = 5
    grey_url    = 5
    Link_Button = 5

    @classmethod
    def from_value(cls, value):
        return try_enum(cls, value)

    # the same as in the class above.
    def __str__(self):
        return getattr(self, 'name')

    def __int__(self):
        return getattr(self, 'value')


class ButtonColor(ButtonStyle):
    """
    :class:`ButtonColor`

    .. note ::
        This is just an Aliase to :class:`ButtonStyle`.
    """
    pass

class InteractionCallbackType(Enum):
    pong = 1
    msg_with_source = 4
    deferred_msg_with_source = 5
    deferred_update_msg = 6
    update_msg = 7

    @classmethod
    def from_value(cls, value):
        return try_enum(cls, value)

    # the same as in the class above.
    def __str__(self):
        return getattr(self, 'name')

    def __int__(self):
        return getattr(self, 'value')


class TimestampStyle(Enum):

    """The Style to use in :meth:`discord.utils.styled_timestamp`

    See Also:  `The Discord-API-Documentation <https://discord.com/developers/docs/reference#message-formating-timestamp-styles>`_
    """

    short_time  = 't'
    long_time   = 'T'
    short_date  = 'd'
    long_date   = 'D'
    short       = 'f'
    long        = 'F'
    relative    = 'R'

    def __repr__(self):
        return getattr(self, 'name')

    def __str__(self):
        return getattr(self, 'value')


    @classmethod
    def from_value(cls, value):
        return try_enum(cls, value)


class MessageType(Enum):
    default                                      = 0
    recipient_add                                = 1
    recipient_remove                             = 2
    call                                         = 3
    channel_name_change                          = 4
    channel_icon_change                          = 5
    pins_add                                     = 6
    new_member                                   = 7
    premium_guild_subscription                   = 8
    premium_guild_tier_1                         = 9
    premium_guild_tier_2                         = 10
    premium_guild_tier_3                         = 11
    channel_follow_add                           = 12
    guild_stream                                 = 13
    guild_discovery_disqualified                 = 14
    guild_discovery_requalified                  = 15
    guild_discovery_grace_period_initial_warning = 16
    guild_discovery_grace_period_final_warning   = 17
    thread_created                               = 18
    reply                                        = 19
    application_command                          = 20
    thread_starter_message                       = 21
    guild_invite_reminder                        = 22


class VoiceRegion(Enum):
    us_west       = 'us-west'
    us_east       = 'us-east'
    us_south      = 'us-south'
    us_central    = 'us-central'
    eu_west       = 'eu-west'
    eu_central    = 'eu-central'
    singapore     = 'singapore'
    london        = 'london'
    sydney        = 'sydney'
    amsterdam     = 'amsterdam'
    frankfurt     = 'frankfurt'
    brazil        = 'brazil'
    hongkong      = 'hongkong'
    russia        = 'russia'
    japan         = 'japan'
    southafrica   = 'southafrica'
    south_korea   = 'south-korea'
    india         = 'india'
    europe        = 'europe'
    dubai         = 'dubai'
    vip_us_east   = 'vip-us-east'
    vip_us_west   = 'vip-us-west'
    vip_amsterdam = 'vip-amsterdam'

    def __str__(self):
        return self.value

class SpeakingState(Enum):
    none       = 0
    voice      = 1
    soundshare = 2
    priority   = 4

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

class VerificationLevel(Enum):
    none              = 0
    low               = 1
    medium            = 2
    high              = 3
    table_flip        = 3
    extreme           = 4
    double_table_flip = 4
    very_high         = 4

    def __str__(self):
        return self.name

class ContentFilter(Enum):
    disabled    = 0
    no_role     = 1
    all_members = 2

    def __str__(self):
        return self.name

class UserContentFilter(Enum):
    disabled    = 0
    friends     = 1
    all_messages = 2

class FriendFlags(Enum):
    noone = 0
    mutual_guilds = 1
    mutual_friends = 2
    guild_and_friends = 3
    everyone = 4

class Theme(Enum):
    light = 'light'
    dark = 'dark'

class Status(Enum):
    online = 'online'
    offline = 'offline'
    idle = 'idle'
    dnd = 'dnd'
    do_not_disturb = 'dnd'
    invisible = 'invisible'

    def __str__(self):
        return self.value

class DefaultAvatar(Enum):
    blurple = 0
    grey    = 1
    gray    = 1
    green   = 2
    orange  = 3
    red     = 4

    def __str__(self):
        return self.name

class RelationshipType(Enum):
    friend           = 1
    blocked          = 2
    incoming_request = 3
    outgoing_request = 4

class NotificationLevel(Enum):
    all_messages  = 0
    only_mentions = 1

class AuditLogActionCategory(Enum):
    create = 1
    delete = 2
    update = 3

class AuditLogAction(Enum):
    guild_update             = 1
    channel_create           = 10
    channel_update           = 11
    channel_delete           = 12
    overwrite_create         = 13
    overwrite_update         = 14
    overwrite_delete         = 15
    kick                     = 20
    member_prune             = 21
    ban                      = 22
    unban                    = 23
    member_update            = 24
    member_role_update       = 25
    member_move              = 26
    member_disconnect        = 27
    bot_add                  = 28
    role_create              = 30
    role_update              = 31
    role_delete              = 32
    invite_create            = 40
    invite_update            = 41
    invite_delete            = 42
    webhook_create           = 50
    webhook_update           = 51
    webhook_delete           = 52
    emoji_create             = 60
    emoji_update             = 61
    emoji_delete             = 62
    message_delete           = 72
    message_bulk_delete      = 73
    message_pin              = 74
    message_unpin            = 75
    integration_create       = 80
    integration_update       = 81
    integration_delete       = 82

    @property
    def category(self):
        lookup = {
            AuditLogAction.guild_update:        AuditLogActionCategory.update,
            AuditLogAction.channel_create:      AuditLogActionCategory.create,
            AuditLogAction.channel_update:      AuditLogActionCategory.update,
            AuditLogAction.channel_delete:      AuditLogActionCategory.delete,
            AuditLogAction.overwrite_create:    AuditLogActionCategory.create,
            AuditLogAction.overwrite_update:    AuditLogActionCategory.update,
            AuditLogAction.overwrite_delete:    AuditLogActionCategory.delete,
            AuditLogAction.kick:                None,
            AuditLogAction.member_prune:        None,
            AuditLogAction.ban:                 None,
            AuditLogAction.unban:               None,
            AuditLogAction.member_update:       AuditLogActionCategory.update,
            AuditLogAction.member_role_update:  AuditLogActionCategory.update,
            AuditLogAction.member_move:         None,
            AuditLogAction.member_disconnect:   None,
            AuditLogAction.bot_add:             None,
            AuditLogAction.role_create:         AuditLogActionCategory.create,
            AuditLogAction.role_update:         AuditLogActionCategory.update,
            AuditLogAction.role_delete:         AuditLogActionCategory.delete,
            AuditLogAction.invite_create:       AuditLogActionCategory.create,
            AuditLogAction.invite_update:       AuditLogActionCategory.update,
            AuditLogAction.invite_delete:       AuditLogActionCategory.delete,
            AuditLogAction.webhook_create:      AuditLogActionCategory.create,
            AuditLogAction.webhook_update:      AuditLogActionCategory.update,
            AuditLogAction.webhook_delete:      AuditLogActionCategory.delete,
            AuditLogAction.emoji_create:        AuditLogActionCategory.create,
            AuditLogAction.emoji_update:        AuditLogActionCategory.update,
            AuditLogAction.emoji_delete:        AuditLogActionCategory.delete,
            AuditLogAction.message_delete:      AuditLogActionCategory.delete,
            AuditLogAction.message_bulk_delete: AuditLogActionCategory.delete,
            AuditLogAction.message_pin:         None,
            AuditLogAction.message_unpin:       None,
            AuditLogAction.integration_create:  AuditLogActionCategory.create,
            AuditLogAction.integration_update:  AuditLogActionCategory.update,
            AuditLogAction.integration_delete:  AuditLogActionCategory.delete,
        }
        return lookup[self]

    @property
    def target_type(self):
        v = self.value
        if v == -1:
            return 'all'
        elif v < 10:
            return 'guild'
        elif v < 20:
            return 'channel'
        elif v < 30:
            return 'user'
        elif v < 40:
            return 'role'
        elif v < 50:
            return 'invite'
        elif v < 60:
            return 'webhook'
        elif v < 70:
            return 'emoji'
        elif v < 80:
            return 'message'
        elif v < 90:
            return 'integration'

class UserFlags(Enum):
    staff = 1
    partner = 2
    hypesquad = 4
    bug_hunter = 8
    mfa_sms = 16
    premium_promo_dismissed = 32
    hypesquad_bravery = 64
    hypesquad_brilliance = 128
    hypesquad_balance = 256
    early_supporter = 512
    team_user = 1024
    system = 4096
    has_unread_urgent_messages = 8192
    bug_hunter_level_2 = 16384
    verified_bot = 65536
    verified_bot_developer = 131072

class ActivityType(Enum):
    unknown = -1
    playing = 0
    streaming = 1
    listening = 2
    watching = 3
    custom = 4
    competing = 5

    def __int__(self):
        return self.value

class HypeSquadHouse(Enum):
    bravery = 1
    brilliance = 2
    balance = 3

class PremiumType(Enum):
    nitro_classic = 1
    nitro = 2

class TeamMembershipState(Enum):
    invited = 1
    accepted = 2

class WebhookType(Enum):
    incoming = 1
    channel_follower = 2

class ExpireBehaviour(Enum):
    remove_role = 0
    kick = 1

ExpireBehavior = ExpireBehaviour

class StickerType(Enum):
    png = 1
    apng = 2
    lottie = 3

def try_enum(cls, val):
    """A function that tries to turn the value into enum ``cls``.

    If it fails it returns the value instead.
    """

    # i use :meth:`getattr` so `codacy` don't cry and *my own* code is as clean as possible.
    try:
        return getattr(cls, '_enum_value_map_')[val]
    except (KeyError, TypeError, AttributeError):
        return val
