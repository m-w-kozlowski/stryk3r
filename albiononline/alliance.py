import aiohttp


from typing import *


class Alliance:
    def __init__(self, id: str) -> None:
        self.id = id
        self.name: str = None
        self.tag: str = None

    @classmethod
    def from_guild_data(cls, data: dict) -> Optional['Alliance']:
        if data['AllianceId'] == "":
            return None
        alliance = Alliance(data['AllianceId'])
        alliance.name = data['AllianceName']
        alliance.tag = data['AllianceTag']
        return alliance

    @classmethod
    def from_character_data(cls, data: dict) -> Optional['Alliance']:
        if data['AllianceId'] == "":
            return None
        alliance = Alliance(data['AllianceId'])
        alliance.name = data['AllianceName']
        alliance.tag = data['AllianceTag']
        return alliance

    async def pull(self, session: Optional[aiohttp.ClientSession]) -> None:
        async with session if session else aiohttp.ClientSession() as s:
            async with s.get('{}'.format(query)) as resp:
                if resp.status != 200:
                    raise ValueError('Request status code: {}'.format(resp.status))
                data = await resp.json()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        tag = "" if self.tag == "" else f' [{self.tag}]'
        return '<Alliance{} {} id="{}">'.format(tag, self.name, self.id)

    def __eq__(self, other: 'Alliance') -> bool:
        return self.id == other.id
