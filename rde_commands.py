import discord
import pymongo
import logging


import rde_client


group_blacklist = discord.app_commands.Group(
    name='blacklist',
    description='Blacklist commands'
)
group_blacklist_user = discord.app_commands.Group(
    name='users',
    description='User blacklist commands',
    parent=group_blacklist
)
group_blacklist_character = discord.app_commands.Group(
    name='characters',
    description='Character blacklist commands',
    parent=group_blacklist
)


@group_blacklist_user.command(
    name='add',
    description='Adds discord user to the blacklist'
)
async def __command_blacklist_add_user(
        interaction: discord.Interaction,
        user: discord.Member,
        reason: str | None
) -> None:
    bl_user = interaction.client.blacklist[user]
    if bl_user.blacklisted():
        await interaction.response.send_message('User is already blacklisted')
        return
    else:
        bl_user.add(reason)
        await interaction.response.send_message(f'Blacklisted {user.mention}')
        logging.warning(' Blacklist: added <User {} id={}> from <Guild "{}" id={}>'.format(
            user.name,
            user.id,
            interaction.guild.name,
            interaction.guild.id
        ))


@group_blacklist_user.command(
    name='remove',
    description='Removes discord user from the blacklist'
)
async def __command_blacklist_remove_user(
        interaction: discord.Interaction,
        user: discord.Member
) -> None:
    bl_user = interaction.client.blacklist[user]
    if not bl_user.blacklisted():
        await interaction.response.send_message('User is not blacklisted')
        return
    bl_user.remove()
    await interaction.response.send_message('Removed user from the blacklist')
    logging.warning(' Blacklist: removed <User {} id={}> from <Guild "{}" id={}>'.format(
        user.name,
        user.id,
        interaction.guild.name,
        interaction.guild.id
    ))


@group_blacklist_character.command(
    name='add',
    description='Adds Albion Online character to blacklist'
)
async def __command_blacklist_add_character(
        interaction: discord.Interaction,
        character: str,
        reason: str | None
) -> None:
    bl_character = interaction.client.blacklist[interaction.guild][character]
    if bl_character.blacklisted():
        await interaction.response.send_message('Character is already blacklisted')
        return
    bl_character.add(reason)
    await interaction.response.send_message('Added character to blacklist')
    logging.warning(' Blacklist: added <Character {}> from <Guild "{}" id={}>'.format(
        character,
        interaction.guild.name,
        interaction.guild.id
    ))


@group_blacklist_character.command(
    name='remove',
    description='Removes Albion Online character from blacklist'
)
async def __command_blacklist_remove_character(
        interaction: discord.Interaction,
        character: str
) -> None:
    bl_character = interaction.client.blacklist[interaction.guild][character]
    if not bl_character.blacklisted():
        await interaction.response.send_message('Character is not blacklisted')
        return
    bl_character.remove()
    await interaction.response.send_message('Removed character from the blacklist')
    logging.warning(' Blacklist: removed <Character {}> from <Guild "{}" id={}>'.format(
        character,
        interaction.guild.name,
        interaction.guild.id
    ))


@group_blacklist_user.command(
    name='list',
    description='Shows all blacklisted users'
)
async def __command_blacklist_users(
        interaction: discord.Interaction
) -> None:
    members = [interaction.guild.get_member(uid) for uid in interaction.client.blacklist[interaction.guild].list_user_ids()]
    if not members:
        await interaction.response.send_message('No blacklisted users')
        return
    resp_content = '**Blacklisted users**\n' + '\n'.join(member.mention for member in members)
    await interaction.response.send_message(resp_content)


@group_blacklist_character.command(
    name='list',
    description='Shows list of blacklisted characters'
)
async def __command_blacklist_characters(
        interaction: discord.Interaction
) -> None:
    members = interaction.client.blacklist[interaction.guild].list_characters()
    if not members:
        await interaction.response.send_message('No blacklisted characters')
        return
    resp_content = '**Blacklisted characters**\n' + '\n'.join(members)
    await interaction.response.send_message(resp_content)


@discord.app_commands.command(
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
    result = interaction.client.register.add(interaction.user, character)
    if result == 'failed-member':
        await interaction.response.send_message('You\'re already registered')
        return
    elif result == 'failed-character':
        await interaction.response.send_message('This character is already registered')
        return
    else:
        await interaction.response.send_message('Successfully registered')


@discord.app_commands.command(
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
    result = interaction.client.register.remove(user)
    if result == 'failed':
        await interaction.response.send_message('User is not registered')
        return
    await interaction.response.send_message('Unregistered user')
