import asyncio

import discord
from discord.ext import commands

COGS = [
    "cogs.core",
]

class MyBot(commands.Bot):
    def __init__(self, prefix, intents, rust_class):
        super().__init__(command_prefix=prefix, intents=intents, help_command=None)
        self.rust_class = rust_class
    
    async def on_ready(self):
        print(f'ready discordBot Logging as {self.user}')

class discordbot():
    async def run_bot(self, rust_class):
        self.bot = MyBot("!",discord.Intents.all(), rust_class)
        for cog in COGS:
            self.bot.load_extension(cog)
        await self.bot.start('')