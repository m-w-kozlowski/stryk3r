import asyncio
import discord
import pymongo


from typing import (
    List,
    Awaitable
)


class Client:
    def __init__(
            self,
            register_collection: pymongo.collection.Collection,
            blacklist_collection: pymongo.collection.Collection
    ) -> None:
        self.register_collection = register_collection
        self.blacklist_collection = blacklist_collection
        self.__verify_user: Awaitable = None

    def verify(
            self,
            guild: discord.Guild
    ) -> List['Result']:
        if not self.__verify_user:
            raise ValueError()

    def user_verification(self, exe: Awaitable) -> None:
        if not asyncio.iscoroutinefunction(exe):
            raise TypeError()
        self.__verify_user = exe


class Result:
    pass
