import pymongo
import discord


from typing import Union, Optional, List


class Member:
    def __init__(self, member: discord.Member, guild: 'Guild') -> None:
        self.member = member
        self.guild = guild
        self.query = {
            'uid': member.id,
            'gid': guild.guild.id
        }

    def data(self) -> Optional[dict]:
        return self.guild.client.user_collection.find_one(self.query)

    def blacklisted(self) -> bool:
        return self.data() is not None

    def reason(self) -> str:
        return self.data()['reason']

    def add(self, reason: str) -> None:
        self.guild.client.user_collection.insert_one({
            'uid': self.member.id,
            'gid': self.guild.guild.id,
            'reason': reason
        })

    def remove(self) -> None:
        self.guild.client.user_collection.delete_one(self.query)


class Character:
    def __init__(self, character: str, guild: 'Guild') -> None:
        self.character = character
        self.guild = guild
        self.query = {
            'cn': character,
            'gid': self.guild.guild.id
        }

    def data(self) -> Optional[dict]:
        return self.guild.client.character_collection.find_one(self.query)

    def blacklisted(self) -> bool:
        return self.data() is not None

    def reason(self) -> str:
        return self.data()['reason']

    def add(self, reason: str) -> None:
        self.guild.client.character_collection.insert_one({
            'cn': self.character,
            'gid': self.guild.guild.id,
            'reason': reason
        })

    def remove(self) -> None:
        self.guild.client.character_collection.delete_one(self.query)


class Guild:
    def __init__(self, guild: discord.Guild, client: 'Client'):
        self.guild = guild
        self.client = client

    def __getitem__(self, item: discord.Member | str) -> Member | Character:
        if isinstance(item, discord.Member):
            return Member(item, self)
        else:
            return Character(item, self)

    def list_user_ids(self) -> List[int]:
        users = self.client.user_collection.find({
            'gid': self.guild.id
        })
        return [user['uid'] for user in users]

    def list_characters(self) -> List[str]:
        characters = self.client.character_collection.find({
            'gid': self.guild.id
        })
        return [character['cn'] for character in characters]


class Client:
    def __init__(self, user_collection: pymongo.collection.Collection, character_collection: pymongo.collection.Collection) -> None:
        self.user_collection = user_collection
        self.character_collection = character_collection

    def __getitem__(self, item: Union[discord.Guild, discord.Member]) -> Union[Member, Guild]:
        if isinstance(item, discord.Guild):
            return Guild(item, self)
        elif isinstance(item, discord.Member):
            return Guild(item.guild, self)[item]