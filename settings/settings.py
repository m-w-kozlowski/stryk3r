import pymongo
import discord

from typing import (
    Callable,
    Any
)


class Setting:
    def __init__(self, collection: pymongo.collection.Collection, gid: int, sid: str, client: 'SettingsClient') -> None:
        self.collection = collection
        self.gid = gid
        self.sid = sid
        self.client = client

    @property
    def __query(self):
        return {
            'gid': self.gid,
            'sid': self.sid
        }

    def __default(self) -> Any:
        try:
            default = self.client.settings[self.sid]
        except KeyError:
            raise NotImplementedError
        if not isinstance(default, Callable):
            raise TypeError()
        return default

    def set(self, __value: dict) -> None:
        if not self.collection.update_one(self.__query, {
            '$set': {
                'v': __value
            }
        }).modified_count:
            self.collection.insert_one({
                'sid': self.sid,
                'gid': self.gid,
                'v': __value
            })

    def __get(self) -> dict:
        query_result = self.collection.find_one(self.__query)
        if query_result is None:
            self.set(self.__default())
        else:
            return query_result
        return self.collection.find_one(self.__query)

    @property
    def value(self):
        return self.__get()['v']


class GuildSettings:
    def __init__(self, collection: pymongo.collection.Collection, guild_id: int, client: 'SettingsClient') -> None:
        self.gid = guild_id
        self.collection = collection
        self.client = client

    def __getitem__(self, item: str) -> Setting:
        return Setting(self.collection, self.gid, item, self.client)


class SettingsClient:
    def __init__(self, collection: pymongo.collection.Collection) -> None:
        self.collection = collection
        self.__settings: dict[str:Callable] = {}

    def __getitem__(self, item: discord.Guild | int) -> GuildSettings:
        gid = item.id if isinstance(item, discord.Guild) else item
        return GuildSettings(self.collection, gid, self)

    def setting(
            self,
            name: str,
    ) -> Callable:
        if name in self.__settings:
            raise ValueError()

        def decorator(function: Callable):
            self.__settings[name] = function
        return decorator

    @property
    def settings(self):
        return self.__settings
