import albiononline
import discord
import aiohttp
import json


from typing import Optional, Any


class Character:
    def __init__(self, id: str) -> None:
        self.id = id
        self.raw_data: dict = None
        self.name: str = None
        self.guild: albiononline.Guild = None
        self.alliance: albiononline.Alliance = None

    async def pull(self, session: Optional[aiohttp.ClientSession] = None) -> None:
        async with session if session else aiohttp.ClientSession() as s:
            async with s.get('https://gameinfo.albiononline.com/api/gameinfo/players/{}'.format(self.id)) as resp:
                if resp.status != 200:
                    raise ValueError('Request status code: {}'.format(resp.status))
                data = await resp.json()
        self.raw_data = data
        self.name = data['Name']
        self.guild = albiononline.Guild.from_character_data(data)
        self.alliance = albiononline.Alliance.from_character_data(data)

    @classmethod
    async def search(cls, query: str, session: Optional[aiohttp.ClientSession] = None) -> 'Character':
        async with session if session else aiohttp.ClientSession() as s:
            async with s.get('https://gameinfo.albiononline.com/api/gameinfo/search?q={}'.format(query)) as resp:
                if resp.status != 200:
                    raise ValueError('Request status code: {}'.format(resp.status))
                search_data = await resp.json()

        # ASSUMPTION: If exact match exists it will be first in query result
        if search_data['players'][0]['Name'] != query:
            return None

        character = Character(search_data['players'][0]['Id'])
        await character.pull()
        return character

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return '<Character {} id="{}">'.format(self.name, self.id)

    def __eq__(self, other: 'Character') -> bool:
        return self.id == other.id
    