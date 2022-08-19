import discord
import rde_client
import logging


def init(client: rde_client.Client) -> None:
    @client.event
    async def on_ready() -> None:
        if not client.synced:
            await client.tree.sync()
            logging.warning(' Synchronized global command tree')
            client.synced = True
            logging.warning(' Client ready')
        logging.warning(f'Connected to {len(client.guilds)} discord guilds:')
        for guild in client.guilds:
            logging.warning(guild)

    @client.event
    async def on_guild_join(guild: discord.Guild) -> None:
        await client.tree.sync(guild=guild)
        logging.warning(f'Synchronized command tree for {guild.__repr__()}')
