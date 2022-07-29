import aiohttp
import pymongo
import discord
import albiononline
import util
from typing import *


def get_registered_character(member: discord.Member, mongo_db_client: pymongo.MongoClient) -> Optional[albiononline.Character]:
    db_data = mongo_db_client['bot']['reg'].find_one({
        'dc.uid': member.id,
        'dc.gid': member.guild.id
    })
    if db_data is None:
        return None
    return albiononline.Character(db_data['ao']['cid'])


class VerifyResult:
    def __init__(
            self,
            member: discord.Member,
            character: discord.Character,
    ) -> None:
        self.member = member
        self.character = character
        self.result = False
        self.code = None

    async def check(
            self,
            target: albiononline.Character,
            mongo_db_client: pymongo.MongoClient,
            session: Optional[aiohttp.ClientSession] = None
    ) -> None:
        character = get_registered_character(self.member, mongo_db_client)
        if character is None:
            self.code = 'NotRegistered'
            return
        await character.pull(session)
        if character.guild == target.guild:
            self.code = 'GuildMatch'
            self.result = True
            return
        if character.alliance == target.alliance:
            self.code = 'AllianceMatch'
            self.result = True
            return
        self.code = 'NotSharedOccupation'

    def __str__(self) -> str:
        return '{} {}'.format(
            self.member.display_name,
            'passed' if self.result else 'failed'
        )

    def __repr__(self) -> str:
        return '<Result {}>'.format(self.member.id)

    def json(self) -> dict:
        return {
            'uid': self.member.id,
            'cid': self.character.id if self.character is not None else None,
            'r': self.result,
            'c': self.code
        }


async def _verification(
        role: discord.Role,
        channel: discord.TextChannel,
        target: albiononline.Character,
        database: pymongo.MongoClient
) -> None:
    """

    :param guild:
    :param role:
    :param channel:
    :return:
    """
    users = []
    for member in role.members:
        db_data = get_registered_character(member, database)
        users.append(VerifyResult(
            member,
            db_data
        ))
    async with aiohttp.ClientSession() as session:
        for user in users:
            await user.check(
                target=target,
                mongo_db_client=database,
                session=session
            )
    message_content = '\n'.join([result.member.mention for result in users])
    await channel.send(message_content)


async def verification(
        database: pymongo.MongoClient
) -> None:

