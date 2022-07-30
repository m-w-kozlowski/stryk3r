import discord
import pymongo
import register
import albiononline
import discord
import blacklist
import settings


class Client(discord.Client):
    def __init__(self, *args, **kwargs) -> None:
        self.synced = False
        self.mongo_client = pymongo.MongoClient(
            host=kwargs.pop('mongo_url'),
            port=kwargs.pop('mongo_port')
        )
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
        super().__init__(*args, **kwargs)
        self.tree = discord.app_commands.CommandTree(self)
