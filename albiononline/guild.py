import albiononline
import discord
import aiohttp


class Guild:
    def __init__(self, id: str) -> None:
        self.id = id
        self.name: str = None
        self.alliance: albiononline.Guild = None

    async def pull(self) -> None:
        pass

    @classmethod
    async def search(cls, query: str) -> 'Guild':
        pass

    @classmethod
    def from_character_data(cls, data: dict) -> 'Guild':
        if data['GuildId'] == "":
            return None
        guild = Guild(data['GuildId'])
        guild.name = data['GuildName']
        guild.alliance = albiononline.Alliance.from_character_data(data)
        return guild

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return '<Guild {} id="{}">'.format(self.name, self.id)

    def __eq__(self, other: 'Guild') -> bool:
        return self.id == other.id
