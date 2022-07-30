# general imports
import os
import aiohttp
import pymongo
import logging

# custom utility imports
from util import *

# RDE imports
import register
import albiononline
import discord
import blacklist
import settings

# typing imports
from typing import (
    Literal,
    Optional,
    Any
)

# project specific imports
import rde_client
import rde_commands
import rde_events

# environment variables
ENV_ALL = (
    'DC_BOT_TOKEN',
    'MONGO_URL',
    'MONGO_PORT',
    'SYNC_COMMANDS'
)
for env_var in ENV_ALL:
    assert env_var in os.environ, 'missing environment variable "{}"'.format(env_var)


# RDE client arguments
intents = discord.Intents.all()
client = rde_client.Client(
    intents=intents,
    mongo_url=os.environ['MONGO_URL'],
    mongo_port=int(os.environ['MONGO_PORT'])
)


# RDE events
rde_events.init(client)


# commands
client.tree.add_command(rde_commands.group_blacklist)
client.tree.add_command(rde_commands.__command_register)
client.tree.add_command(rde_commands.__command_unregister)


# settings
@client.settings.setting('albion-online-role')
def __default_setting_albion_online_role():
    return None


# RDE run
client.run(os.environ['DC_BOT_TOKEN'])
