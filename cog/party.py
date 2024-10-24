import discord
from discord.ext import commands
from discord import app_commands
import datetime

class joiner(discord.ui.View):
    def __init__(self, disable_callout=False):
        super().__init__(timeout=None)
        self.embed_value = None
        self.add_item(discord.ui.Button(label="参加", emoji="<:Blob_join:1168831929567674418>", style=discord.ButtonStyle.green, custom_id="join"))
        callout_button = discord.ui.Button(label="呼び出し", emoji="📢", style=discord.ButtonStyle.primary, custom_id="callout")
        if disable_callout:
            callout_button.disabled = True
        self.add_item(callout_button)
        self.add_item(discord.ui.Button(label="編集", emoji="✏️", style=discord.ButtonStyle.gray, custom_id="edit"))

class callout_confirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="はい", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

    @discord.ui.button(label="いいえ", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()

class creater(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="パーティー作成", timeout=None)
        self.value=None

        self.name = discord.ui.TextInput(
            label="名前",
            style=discord.TextStyle.short,
            placeholder="まいくら",
            required=True
        )
        self.time = discord.ui.TextInput(
            label="開始時刻",
            style=discord.TextStyle.short,
            placeholder="19時",
            required=True
        )
        self.users = discord.ui.TextInput(
            label="人数",
            style=discord.TextStyle.short,
            placeholder="5人",
            required=True
        )
        self.add_item(self.name)
        self.add_item(self.time)
        self.add_item(self.users)
    
    async def on_submit(self, interaction:discord.Interaction):
        embed = discord.Embed(title=f"募集：{self.name.value}", description=f"{interaction.user.mention}が{self.name.value}を募集中です！", timestamp=datetime.datetime.now())
        embed.add_field(name="開始時刻", value=f"{self.time.value}", inline=False)
        embed.add_field(name="人数", value=f"{self.users.value}", inline=False)
        embed.add_field(name="参加者", value=f"{interaction.user.mention}", inline=False)
        embed.add_field(name="", value=f"📢 </game:1169850101410308116> で参加者を募集！", inline=False)
        embed.set_author(name=f"{interaction.user.display_name}", icon_url=interaction.user.avatar.url)
        embed.set_footer(text=f"ID: {interaction.user.id}")
        await interaction.channel.send(embed=embed, view=joiner())
        self.stop()
        await interaction.response.send_message("作成しました！", ephemeral=True)

class editor(discord.ui.Modal):
    def __init__(self, old_time, old_users):
        super().__init__(title="パーティー編集", timeout=None)
        self.value = None

        self.time = discord.ui.TextInput(
            label="開始時刻",
            style=discord.TextStyle.short,
            placeholder="19時",
            required=True,
            default=old_time
        )
        self.users = discord.ui.TextInput(
            label="人数",
            style=discord.TextStyle.short,
            placeholder="5人",
            required=True,
            default=old_users
        )
        self.add_item(self.time)
        self.add_item(self.users)

    async def on_submit(self, interaction: discord.Interaction):
        self.value = {
            "time": self.time.value,
            "users": self.users.value
        }
        await interaction.response.defer()
        self.stop()

class party(commands.Cog):
    def __init__(self, client):
        self.bot = client
        self.embed_value = None
        self.callout_used = {}
        
    @app_commands.command(name="game", description="ゲームを募集します")
    async def p_create(self, interaction:discord.Interaction):
        await interaction.response.send_modal(creater())

    @commands.Cog.listener()
    async def on_interaction(self, inter:discord.Interaction):
        try:
            if inter.data['component_type'] == 2:
                await self.on_button_click(inter)
            elif inter.data['component_type'] == 3:
                await self.on_dropdown(inter)
        except KeyError:
            pass
    
    async def on_button_click(self, interaction:discord.Interaction):
        custom_id = interaction.data["custom_id"]
        if custom_id == "join":
            ori_msg = interaction.message
            embed = ori_msg.embeds[0]
            val_list = embed.fields[2].value.split("\n")
            if interaction.user.mention in val_list:
                val_list.remove(interaction.user.mention)
                new_value = "\n".join(val_list)
                embed.set_field_at(2, name="参加者", value=new_value)
                await ori_msg.edit(embed=embed)
                await interaction.response.send_message("参加をキャンセルしました！", ephemeral=True)
            else:
                new_value = f"{embed.fields[2].value}\n{interaction.user.mention}"
                embed.set_field_at(2, name="参加者", value=new_value)
                await ori_msg.edit(embed=embed)
                await interaction.response.send_message("参加しました！\n再度ボタンを押すことで参加をキャンセルできます。", ephemeral=True)
        elif custom_id == "create":
            await interaction.response.send_modal(creater())
        elif custom_id == "callout":
            embed = interaction.message.embeds[0]
            creator_id = int(embed.footer.text.split(": ")[1])
            
            if interaction.user.id != creator_id:
                await interaction.response.send_message("呼び出しは募集した人のみが行えます。", ephemeral=True)
                return

            view = callout_confirm()
            await interaction.response.send_message("メンションで参加者を呼び出します。呼び出しは１回だけ利用できます。本当に使いますか？", view=view, ephemeral=True)
            await view.wait()

            if view.value:
                participants = embed.fields[2].value.split("\n")
                mentions = " ".join(participants)
                callout_message = f"{mentions}\n\n**呼び出しが行われました！**\n\n"

                await interaction.message.reply(callout_message)
                self.callout_used[interaction.message.id] = True
                
                ori_msg = interaction.message
                view = joiner(disable_callout=True)
                for item in view.children:
                    if item.custom_id == "callout":
                        item.disabled = True
                await ori_msg.edit(view=view)
                
                await interaction.followup.send("呼び出しを行いました。", ephemeral=True)
            else:
                await interaction.followup.send("呼び出しをキャンセルしました。", ephemeral=True)
        elif custom_id == "edit":
            embed = interaction.message.embeds[0]
            creator_id = int(embed.footer.text.split(": ")[1])
            
            if interaction.user.id != creator_id:
                await interaction.response.send_message("編集は募集した人のみが行えます。", ephemeral=True)
                return

            old_time = embed.fields[0].value
            old_users = embed.fields[1].value

            modal = editor(old_time, old_users)
            await interaction.response.send_modal(modal)
            await modal.wait()

            if modal.value:
                new_time = modal.value["time"]
                new_users = modal.value["users"]

                embed.set_field_at(0, name="開始時刻", value=f"{old_time} ▶ {new_time}" if old_time != new_time else new_time, inline=False)
                embed.set_field_at(1, name="人数", value=f"{old_users} ▶ {new_users}" if old_users != new_users else new_users, inline=False)
                
                author_name = embed.author.name
                if not author_name.endswith("(編集済み)"):
                    embed.set_author(name=f"{author_name} (編集済み)", icon_url=embed.author.icon_url)

                await interaction.message.edit(embed=embed)
                await interaction.followup.send("募集内容を編集しました。", ephemeral=True)

    async def on_dropdown(self, inter: discord.Interaction):
        custom_id = inter.data["custom_id"]
        select_values = inter.data["values"]
        print(custom_id)
        await inter.response.send_message("Select!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(party(bot))
