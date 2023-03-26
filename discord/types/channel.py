# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2021-present mccoderpy

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
from __future__ import annotations

from typing import (
    List,
    Optional
)

from typing_extensions import (
    Literal,
    NotRequired,
    TypedDict
)

from .snowflake import SnowflakeID

__all__ = (
    'ChannelType',
    'Overwrite',
    'GuildChannel',
    'ThreadMetadata',
    'PartialChannel'
)

ChannelType = Literal[0, 1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15]


class Overwrite(TypedDict):
    id: SnowflakeID
    type: Literal[0, 1]
    allow: str
    deny: str


class GuildChannel(TypedDict):
    id: SnowflakeID
    type: ChannelType
    name: NotRequired[Optional[str]]
    position: NotRequired[int]
    parent_id: NotRequired[Optional[SnowflakeID]]
    permission_overwrites: NotRequired[List[Overwrite]]


class ThreadMetadata(TypedDict):
    archived: bool
    auto_archive_duration: int
    archive_timestamp: str
    locked: bool
    invitable: NotRequired[bool]
    create_timestamp: NotRequired[Optional[str]]


class PartialChannel(TypedDict):
    id: SnowflakeID
    type: ChannelType
    name: NotRequired[Optional[str]]
    # TODO: What fields are missing here?