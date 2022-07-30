import discord
import pymongo
import time
from typing import (
    Union,
    Optional,
    Literal
)


class Entry:
    def __init__(
            self,
            character_name: str,
            member: discord.Member,
            timestamp: int
    ) -> None:
        self.character_name = character_name
        self.member = member
        self.timestamp = timestamp


class Client:
    def __init__(
            self,
            collection: pymongo.collection.Collection
    ) -> None:
        self.collection = collection

    def user_info(
            self,
            member: discord.Member
    ) -> Optional[Entry]:
        query_result = self.collection.find_one({
            'gid': member.guild.id,
            'uid': member.id
        })
        if not query_result:
            return None
        else:
            return Entry(
                query_result['cn'],
                member,
                query_result['t']
            )

    def add(
            self,
            member: discord.Member,
            character_name: str
    ) -> Literal['succes', 'failed-member', 'failed-character']:
        if self.collection.find_one({
            'uid': member.id,
            'gid': member.guild.id
        }):
            return 'failed-member'
        elif self.collection.find_one({
            'cn': character_name,
            'gid': member.guild.id
        }):
            return 'failed-character'
        else:
            self.collection.insert_one({
                'cn': character_name,
                'uid': member.id,
                'gid': member.guild.id,
                't': int(time.time())
            })
            return 'success'

    def remove(
            self,
            ctx: Union[discord.Member, str],
            guild: Optional[discord.Guild] = None
    ) -> Literal['success', 'failed']:
        if isinstance(ctx, discord.Member):
            deleted = self.collection.delete_one({
                'uid': ctx.id,
                'gid': ctx.guild.id
            })
            if deleted.deleted_count:
                return 'success'
            else:
                return 'failed'
        elif isinstance(ctx, str):
            if not guild:
                raise TypeError()
            deleted = self.collection.delete_one({
                'cn': ctx,
                'gid': guild.id
            })
            if deleted.deleted_count:
                return 'success'
            else:
                return 'failed'
