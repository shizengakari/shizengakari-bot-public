import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, time, timedelta

class onecomment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channels = [
            # チャンネルIDを追加
        ]
        self.messages = {channel_id: {} for channel_id in self.channels}
        self.embeds = {channel_id: None for channel_id in self.channels}
        self.ranking.start()

    def is_time_in_range(self, start, end, x):
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    def time_difference_from_midnight(self, time_str):
        hours = int(time_str[:2])
        minutes = int(time_str[2:4])
        seconds = int(time_str[4:6])
        microseconds = int(time_str[6:])
        if hours == 23:
            return abs((3600 * 24) - (hours * 3600 + minutes * 60 + seconds + microseconds / 1000000))
        else:
            return abs(hours * 3600 + minutes * 60 + seconds + microseconds / 1000000)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id in self.channels:
            if message.author.bot:
                return
            channel_messages = self.messages[message.channel.id]
            if message.author.id in channel_messages:
                return
            msg_time = message.created_at + timedelta(hours=9)
            if self.is_time_in_range(time(23, 59), time(0, 1), msg_time.time()):
                self.messages[message.channel.id][message.author.id] = (
                    message.author.id,
                    (message.created_at + timedelta(hours=9)).strftime('%H%M%S%f'),
                    message.id
                )

    @tasks.loop()
    async def ranking(self):
        now = datetime.now()
        if now.strftime("%H:%M") == "00:01":
            for channel_id in self.channels:
                channel = self.bot.get_channel(channel_id)
                if channel and self.embeds[channel_id] is None:
                    try:
                        channel_messages = self.messages[channel_id]
                        if not channel_messages:
                            self.embeds[channel_id] = "空のランキング"
                            continue
                        
                        # 0時からの差で並び替え
                        sorted_messages = sorted(
                            channel_messages.items(),
                            key=lambda x: self.time_difference_from_midnight(x[1][1])
                        )
                        rank_message = "> 0:00に一番近く送ったメッセージランキング\n"
                        for i, msg in enumerate(sorted_messages):
                            rank_message += f"{i+1}位. <@{msg[1][0]}> 送信時間:{msg[1][1][:2]}:{msg[1][1][2:4]}:{msg[1][1][4:6]}.{msg[1][1][6:]} [Link](https://discord.com/channels/{channel.guild.id}/{channel_id}/{msg[1][2]})\n"
                        self.embeds[channel_id] = await channel.send(
                            embed=discord.Embed(
                                title="一コメランキング",
                                description=rank_message,
                                timestamp=now,
                                color=discord.Color.blue()
                            ).set_footer(text="この機能はβ版です。")
                        )
                        self.messages[channel_id] = {}
                    except Exception as e:
                        self.embeds[channel_id] = await channel.send(
                            content="<@964887498436276305>",
                            embed=discord.Embed(
                                title="エラー",
                                description=f"送信する際にエラーが発生しました。\nエラー内容：`{e}`",
                                color=discord.Color.red()
                            )
                        )

        elif now.strftime("%H:%M") == "23:59":
            for channel_id in self.channels:
                channel = self.bot.get_channel(channel_id)
                if channel and self.embeds[channel_id] is None:
                    self.embeds[channel_id] = await channel.send(
                        content="0時だよ！全員集合！",
                        embed=discord.Embed(
                            title="一コメランキング",
                            description=f"0時ちょうどにメッセージを送って明日の一コメを決めましょう。\n計測中...結果は{discord.utils.format_dt((now+timedelta(days=1)).replace(hour=0, minute=1, second=0, microsecond=0))}に送信されます。",
                            color=discord.Color.blue()
                        )
                    )
        else:
            for channel_id in self.channels:
                self.embeds[channel_id] = None

    async def cog_unload(self):
        self.ranking.stop()

async def setup(bot: commands.Bot):
    await bot.add_cog(onecomment(bot))
