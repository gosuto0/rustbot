from operator import contains
from tkinter import E
from discord.ext import commands
import discord
import platform
from discord.ext.commands import has_permissions
from discord.ext import tasks
import datetime
from datetime import timedelta

class CoreCog(commands.Cog):
    def __init__(self, bot):
        global instance
        self.bot = bot
        self.attack_heli = "Unknown"
        self.now_attack_heli = False

    @commands.command()
    async def ping(self, ctx):
        os = platform.system()
        ver = platform.release()
        ping = round(self.bot.latency * 1000)
        await ctx.send("OS: " + os + "\nVersion: " + ver + "\nPing: " + str(ping) + "ms", delete_after=10)

    @commands.command()
    async def start(self, ctx):
        embed = await self.get_embed()
        self.message = await ctx.send(embed=embed)
        self.refresh_message.start()

    @tasks.loop(seconds=3)
    async def refresh_message(self):
        try:
            embed = await self.get_embed()
            raidcheck = await self.bot.rust_class.raid_check()
            await self.message.edit(embed=embed)
            if raidcheck:
                await self.message.channel.send("@everyone E13メインベースレイド!!")
        except Exception as e: print("Return Error: "+str(e))
        
    async def refresh_data(self):
        self.server_info = await self.bot.rust_class.get_serverinfo()
        self.server_time = await self.bot.rust_class.get_servertime()
        try:
            self.server_infoorg = str(self.server_info.players)+"/"+str(self.server_info.max_players)+"("+str(self.server_info.queued_players)+")"
            self.server_nameorg = self.server_info.name
            self.server_timeorg = self.server_time.time
            self.server_sunorg = self.server_time.sunrise+" - "+self.server_time.sunset
            self.server_event = await self.organize_serverevent()
            self.server_wipe = datetime.datetime.fromtimestamp(self.server_info.wipe_time)+ timedelta(days=30)
        except Exception as e:
            self.server_infoorg = "Restarting?"
            self.server_timeorg = "Restarting?"
            self.server_nameorg = "Restaring?"
            self.server_sunorg = "Restarting?"
            self.server_event = "Restarting?"
            self.server_wipe = "Restarting?"
            self.attack_heli = "Restarting?"
            print(str(e))
            
    async def get_embed(self):
        await self.refresh_data()
        embed = discord.Embed(title=self.server_nameorg,description="")
        embed.add_field(name="プレイヤー数 現在/最大(待機)", value=self.server_infoorg,inline=False)
        embed.add_field(name="サーバー内時間",value=self.server_timeorg,inline=False)
        embed.add_field(name="日の出 - 日没",value=self.server_sunorg,inline=False)
        embed.add_field(name="現在のイベント",value=self.server_event,inline=False)
        embed.add_field(name="ワイプ",value=self.server_wipe,inline=False)
        embed.add_field(name="ｶﾞﾁﾍﾘ情報", value=self.attack_heli,inline=False)
        return embed

    async def organize_serverevent(self):
        server_event = await self.bot.rust_class.get_serverevent()
        event_strlist = ""
        event_list = []
        dt_now = datetime.datetime.now()
        dt_after1 = datetime.datetime.now()+timedelta(hours=3)
        for event in server_event:
            event_list.append(str(event.type))
            if event.type == 4:
                event_strlist = event_strlist+"CH-47, "
            if event.type == 5:
                event_strlist = event_strlist+"貨物船, "
            if event.type == 8:
                event_strlist = event_strlist+"アタックヘリコプター, "
                self.now_attack_heli = True
        if "8" not in event_list:
            if self.now_attack_heli == True:
                if event.type != 8:
                    self.now_attack_heli = False
                    self.attack_heli = "ｶﾞﾁﾍﾘ爆発 "+str(dt_now.strftime('%H:%M:%S'))+" 再沸き "+str(dt_after1.strftime('%H:%M:%S'))
        if event_strlist == "":
            return "No Event"
        return event_strlist

def setup(bot):
    bot.add_cog(CoreCog(bot))