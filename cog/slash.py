import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

import random
import asyncio
import datetime
import requests

class reget(discord.ui.View):
    def __init__(self, bot, user_id):
        super().__init__()
        self.bot = bot
        self.user_id = user_id
        self.agent = ["フェニックス", "ジェット", "スカイ", "ネオン", "ヨル", "サイファー", "キルジョイ", "チェンバー",
                      "セージ", "KAY/O", "オーメン", "ブリーチ", "ソーヴァ", "アイソ", "ブリーチ", 
                      "キルジョイ", "ゲッコー", "ハーバー", "アストラ", "ヴァイパー", "ブリムストーン", "デットロック", "フェイド", "クローヴ", "ヴァイス"]
        self.weapon = ["クラシック", "ショーティー", "フレンジー", "ゴースト", "シェリフ", "スティンガー", "スペクター", "ジャッジ", "バッキー", 
                      "ガーディアン", "ファントム", "ヴァンダル", "オペレーター", "マーシャル", "アレス", "オーディン", "ナイフ"]
        self.server = ["TOKYO", "HongKong", "Sydney", "Mumbai", "Singapore"]
        self.map = ["アイスボックス", "サンセット", "アセント", "ブリーズ", "ヘイブン", "ロータス", "バインド", "スプリット", "フラクチャー", "パール", "アビス"]
        self.gamemode = ["アンレート", "コンペティティブ", "スイフトプレイ", "スパイクラッシュ", "デスマッチ", "エスカレーション", "チームデスマッチ"]

    @discord.ui.button(label="もういっかい！", emoji="🔁", style=discord.ButtonStyle.green)
    async def re_random(self, interaction, button: discord.ui.Button):
        ori_msg = interaction.message
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(f"スラッシュコマンドを実行した人のみボタンを押せます", ephemeral=True)
            return
        if "エージェント" in ori_msg.content:
            choice = random.choice(self.agent)
            await ori_msg.edit(content=f"エージェント：{choice}")
            await interaction.response.send_message(f"もう一回ランダムで選びました。\n選択したもの：{choice}", ephemeral=True)
            return
        elif "武器" in ori_msg.content:
            choice = random.choice(self.weapon)
            await ori_msg.edit(content=f"武器：{choice}")
            await interaction.response.send_message(f"もう一回ランダムで選びました。\n選択したもの：{choice}", ephemeral=True)
            return
        elif "サーバー" in ori_msg.content:
            choice = random.choice(self.server)
            await ori_msg.edit(content=f"サーバー：{choice}")
            await interaction.response.send_message(f"もう一回ランダムで選びました\n選択したもの：{choice}", ephemeral=True)
            return
        elif "ゲームモード" in ori_msg.content:
            choice = random.choice(self.gamemode)
            await ori_msg.edit(content=f"ゲームモード：{choice}")
            await interaction.response.send_message(f"もう一回ランダムで選びました。\n選択したもの：{choice}", ephemeral=True)
            return
        elif "マップ" in ori_msg.content:
            choice = random.choice(self.map)
            await ori_msg.edit(content=f"マップ：{choice}")
            await interaction.response.send_message(f"もう一回ランダムで選びました。\n選択したもの：{choice}", ephemeral=True)
            return
        elif "感度" in ori_msg.content:
            choice = random.uniform(0.1, 1)
            await ori_msg.edit(content=f"感度：{choice:.2f}")
            await interaction.response.send_message(f"もう一回ランダムで選びました。\n選択したもの：{choice}", ephemeral=True)
            return
        elif "ランダム結果" == ori_msg.embeds[0].title:
            await ori_msg.edit(embed=discord.Embed(title="ランダム結果", timestamp=datetime.datetime.now()).add_field(
            name="エージェント", value=random.choice(self.agent)
            ).add_field(name="銃", value=random.choice(self.weapon)
            ).add_field(name="サーバー", value=random.choice(self.server)
            ).add_field(name="感度", value=f"{random.uniform(0.1, 1):.2f}"
            ).add_field(name="マップ", value=random.choice(self.map)
            ).add_field(name="ゲームモード", value=random.choice(self.gamemode)))
            await interaction.response.send_message(f"もう一回ランダムで選びました。選んだものは[リプライ先]({ori_msg.jump_url})のものです。", ephemeral=True)
        
    
class slash(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
        self.agent = ["フェニックス", "ジェット", "スカイ", "ネオン", "ヨル", "サイファー", "キルジョイ", "チェンバー", "セージ", "KAY/O", "オーメン", "ブリーチ", "ソーヴァ", "アイソ", "ブリーチ", 
            "キルジョイ", "ゲッコー", "ハーバー", "アストラ", "ヴァイパー", "ブリムストーン", "デットロック", "フェイド", "クローヴ", "ヴァイス"]
        self.weapon = ["クラシック", "ショーティー", "フレンジー", "ゴースト", "シェリフ", "スティンガー", "スペクター", "ジャッジ", "バッキー", 
                "ガーディアン", "ファントム", "ヴァンダル", "オペレーター", "マーシャル", "アレス", "オーディン", "ナイフ"]
        self.server = ["Tokyo", "HongKong", "Sydney", "Mumbai", "Singapore"]
        self.map = ["アイスボックス", "サンセット", "アセント", "ブリーズ", "ヘイブン", "ロータス", "バインド", "スプリット", "フラクチャー", "パール", "アビス"]
        self.gamemode = ["アンレート", "コンペティティブ", "スイフトプレイ", "スパイクラッシュ", "デスマッチ", "エスカレーション", "チームデスマッチ"]

    group = app_commands.Group(name="valorant", description="Valorant関係", guild_only=False)

    @group.command(name="agent", description="エージェントをランダムで選びます")
    async def agent_random(self, interaction):
        await interaction.response.send_message(f"エージェント：{random.choice(self.agent)}", view=reget(self, interaction.user.id))

    @group.command(name="weapon", description="武器をランダムで選びます")
    async def weapon_random(self, interaction):
        await interaction.response.send_message(f"武器：{random.choice(self.weapon)}", view=reget(self, interaction.user.id))

    @group.command(name="server", description="サーバーをランダムで選びます")
    async def server_random(self, interaction):
        await interaction.response.send_message(f"サーバー：{random.choice(self.server)}", view=reget(self, interaction.user.id))

    @group.command(name="sensitivity", description="感度をランダムで選びます")
    async def sensitvity_random(self, interaction):
        await interaction.response.send_message(f"感度：{random.uniform(0.1, 1):.2f}", view=reget(self, interaction.user.id))

    @group.command(name="map", description="マップをランダムで選びます")
    async def map_random(self, interaction):
        await interaction.response.send_message(f"マップ：{random.choice(self.map)}", view=reget(self, interaction.user.id))

    @group.command(name="gamemode", description="ゲームモードをランダムで選びます")
    async def gamemode_random(self, interaction):
        await interaction.response.send_message(f"ゲームモード：{random.choice(self.gamemode)}", view=reget(self, interaction.user.id))
    
    @group.command(name="all", description="すべてをランダムで選びます")
    async def all_random(self, interaction):
        await interaction.response.send_message(embed=discord.Embed(title="ランダム結果", timestamp=datetime.datetime.now()).add_field(
        name="エージェント", value=random.choice(self.agent)
        ).add_field(name="銃", value=random.choice(self.weapon)
        ).add_field(name="サーバー", value=random.choice(self.server)
        ).add_field(name="感度", value=f"{random.uniform(0.1, 1):.2f}"
        ).add_field(name="マップ", value=random.choice(self.map)
        ).add_field(name="ゲームモード", value=random.choice(self.gamemode)), view=reget(self, interaction.user.id))

    @app_commands.command(name="shorten", description="URLを短縮します")
    @app_commands.describe(url="短縮するURL")
    async def shorten(self, interaction:discord.Interaction, url:str):
        if not url.startswith("http"):
            await interaction.response.send_message("URLが不正です",ephemeral=True)
            return
        headers = {
            "Content-Type":"application/json"
        }
        data = {
            "url":url
        }
        await interaction.response.defer(ephemeral=True) # bot is thinking...🤔
        try:
            response = requests.post("https://st.shizen.lol/shorten",json=data, headers=headers, timeout=(3.0, 5.0))
        except requests.exceptions.Timeout:
            await interaction.followup.send("APIサーバーへのアクセスがタイムアウトしました。",ephemeral=True)
        if response.status_code != 200:
            await interaction.followup.send(f"エラーが発生しました。\nエラー: {'APIサーバーがダウンしています。' if response.status_code == 502 else 'APIサーバー内でエラーが発生しました。'}",ephemeral=True)
            return
        else:
            await interaction.followup.send(f'リンクを生成しました！\n{response.json()["url"]}',
            view=discord.ui.View().add_item(discord.ui.Button(label="飛んでみる！",url=response.json()['url'], style=discord.ButtonStyle)),ephemeral=True)

async def setup(bot: commands.Bot):
  await bot.add_cog(slash(bot))
