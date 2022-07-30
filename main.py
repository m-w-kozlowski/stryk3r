import os
import aiohttp
import pymongo
import  register
import albiononline
import discord
from util import *
from typing import Literal
from typing import Optional
from typing import Any
import blacklist
import settings


assert 'DC_BOT_TOKEN' in os.environ


MONGO_URL = os.environ['MONGO_URL']
MONGO_PORT = int(os.environ['MONGO_PORT'])


class CustomClient(discord.Client):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.synced = False
        self.mongo_client = pymongo.MongoClient(host=MONGO_URL, port=MONGO_PORT)
        self.blacklist = blacklist.Client(
            self.mongo_client['bot']['user_blacklist'],
            self.mongo_client['bot']['character_blacklist']
        )
        self.settings = settings.SettingsClient(
            self.mongo_client['bot']['settings']
        )
        self.register = register.Client(
            self.mongo_client['bot']['registered']
        )


intents = discord.Intents.all()
client = CustomClient(
    intents=intents
)
tree = discord.app_commands.CommandTree(
    client=client
)


@client.settings.setting('albion-online-role')
def __default_setting_albion_online_role():
    return None


@tree.command(
    name='blacklist-add-user',
    description='Adds discord user to the blacklist'
)
async def __command_blacklist_add_user(
        interaction: discord.Interaction,
        user: discord.Member,
        reason: str | None
) -> None:
    bl_user = client.blacklist[user]
    if bl_user.blacklisted():
        await interaction.response.send_message('User is already blacklisted')
        return
    else:
        bl_user.add(reason)
        await interaction.response.send_message(f'Blacklisted {user.mention}')


@tree.command(
    name='blacklist-remove-user',
    description='Removes discord user from the blacklist'
)
async def __command_blacklist_remove_user(
        interaction: discord.Interaction,
        user: discord.Member
) -> None:
    bl_user = client.blacklist[user]
    if not bl_user.blacklisted():
        await interaction.response.send_message('User is not blacklisted')
        return
    bl_user.remove()
    await interaction.response.send_message('Removed user from the blacklist')


@tree.command(
    name='blacklist-users',
    description='Shows all blacklisted users'
)
async def __command_blacklist_users(
        interaction: discord.Interaction
) -> None:
    members = [interaction.guild.get_member(uid) for uid in client.blacklist[interaction.guild].list_user_ids()]
    if not members:
        await interaction.response.send_message('No blacklisted users')
        return
    resp_content = '**Blacklisted users**\n' + '\n'.join(member.mention for member in members)
    await interaction.response.send_message(resp_content)


@tree.command(
    name='blacklist-add-character',
    description='Adds Albion Online character to blacklist'
)
async def __command_blacklist_add_character(
        interaction: discord.Interaction,
        character: str,
        reason: str | None
) -> None:
    bl_character = client.blacklist[interaction.guild][character]
    if bl_character.blacklisted():
        await interaction.response.send_message('Character is already blacklisted')
        return
    bl_character.add(reason)
    await interaction.response.send_message('Added character to blacklist')


@tree.command(
    name='blacklist-remove-character',
    description='Removes Albion Online character from blacklist'
)
async def __command_blacklist_remove_character(
        interaction: discord.Interaction,
        character: str
) -> None:
    bl_character = client.blacklist[interaction.guild][character]
    if not bl_character.blacklisted():
        await interaction.response.send_message('Character is not blacklisted')
        return
    bl_character.remove()
    await interaction.response.send_message('Removed character from the blacklist')


@tree.command(
    name='blacklist-characters',
    description='Shows list of blacklisted characters'
)
async def __command_blacklist_characters(
        interaction: discord.Interaction
) -> None:
    members = client.blacklist[interaction.guild].list_characters()
    if not members:
        await interaction.response.send_message('No blacklisted characters')
        return
    resp_content = '**Blacklisted characters**\n' + '\n'.join(members)
    await interaction.response.send_message(resp_content)


@tree.command(
    name='register',
    description='Registers albion online character'
)
async def __command_register(
        interaction: discord.Interaction,
        character: str
) -> None:
    if interaction.guild is None:
        await interaction.response.send_message('You\'re trying to use server-only command')
        return
    if not await albiononline.Character.search(character):
        await interaction.response.send_message('Such character does not exist')
        return
    result = client.register.add(interaction.user, character)
    if result == 'failed-member':
        await interaction.response.send_message('You\'re already registered')
        return
    elif result == 'failed-character':
        await interaction.response.send_message('This character is already registered')
        return
    else:
        await interaction.response.send_message('Successfully registered')


@tree.command(
    name='unregister',
    description='Unregister user'
)
async def __command_unregister(
        interaction: discord.Interaction,
        user: discord.Member
) -> None:
    if interaction.guild is None:
        await interaction.response.send_message('You\'re trying to use server-only command')
        return
    result = client.register.remove(user)
    if result == 'failed':
        await interaction.response.send_message('User is not registered')
        return
    await interaction.response.send_message('Unregistered user')


@client.event
async def on_ready() -> None:
    if not client.synced:
        if os.environ['SYNC_COMMANDS']:
            await tree.sync()
            client.synced = True


client.run(os.environ['DC_BOT_TOKEN'])
