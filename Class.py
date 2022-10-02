import discord
from discord.ext import commands
from discord.ui import Modal, TextInput
from Function import *
import random


class bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True
        super().__init__(command_prefix='.', intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(Tester())
        self.add_view(ControlPanel())
        await self.tree.sync(guild=discord.Object(id="1020640631175004160"))
        print(f"Synced slash commands for {self.user}.")

    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral=True)


class NameModal(Modal, title="Name for channel"):
    name = TextInput(label="Name", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.user.voice.channel.edit(name=self.name.value)
        await interaction.response.send_message("")


class SCPModal(Modal, title="SET COUNT PEOPLE (0-infinity)"):
    scp = TextInput(label="Count")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.user.voice.channel.edit(user_limit=int(self.scp.value))
        await interaction.response.send_message("")


class ControlPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(custom_id='persistent_view:name_bt', label='Name', style=discord.ButtonStyle.blurple)
    async def name_bt(self, interaction: discord.Interaction, button:discord.Button):
        if interaction.user.voice is None:
            await interaction.response.send_message("Ви не знаходитесь у голосовому каналі", ephemeral=True)
        elif (str(interaction.user.voice.channel.category.id) == "1020763715836059699" or str(
                interaction.user.voice.channel.category.id) == "852919409952423966"):
            await interaction.response.send_modal(NameModal())
        else:
            await interaction.response.send_message("Канал, в якому ви знаходитесь, неможна змінювати", ephemeral=True)

    @discord.ui.button(custom_id='persistent_view:lock_bt', label='Lock', style=discord.ButtonStyle.blurple)
    async def lock_bt(self, interaction: discord.Interaction, button:discord.Button):
        role = interaction.guild.default_role
        if interaction.user.voice is None:
            await interaction.response.send_message("Ви не знаходитесь у голосовому каналі", ephemeral=True)
        elif (str(interaction.user.voice.channel.category.id) == "1020763715836059699" or str(
                interaction.user.voice.channel.category.id) == "852919409952423966"):
            await interaction.user.voice.channel.set_permissions(role, connect=False)
            await interaction.response.send_message(" ")
        else:
            await interaction.response.send_message("Канал, в якому ви знаходитесь, неможна змінювати", ephemeral=True)

    @discord.ui.button(custom_id='persistent_view:unlock_bt', label='Unlock', style=discord.ButtonStyle.blurple)
    async def unlock_bt(self, interaction: discord.Interaction, button:discord.Button):
        role = interaction.guild.default_role
        if interaction.user.voice is None:
            await interaction.response.send_message("Ви не знаходитесь у голосовому каналі", ephemeral=True)
        elif (str(interaction.user.voice.channel.category.id) == "1020763715836059699" or str(
                interaction.user.voice.channel.category.id) == "852919409952423966"):
            await interaction.user.voice.channel.set_permissions(role, connect=True)
            await interaction.response.send_message(" ")
        else:
            await interaction.response.send_message("Канал, в якому ви знаходитесь, неможна змінювати", ephemeral=True)

    @discord.ui.button(custom_id='persistent_view:scp_bt', label='SCP', style=discord.ButtonStyle.blurple)
    async def scp_bt(self, interaction: discord.Interaction, button:discord.Button):
        if interaction.user.voice is None:
            await interaction.response.send_message("Ви не знаходитесь у голосовому каналі", ephemeral=True)
        elif (str(interaction.user.voice.channel.category.id) == "1020763715836059699" or str(
                interaction.user.voice.channel.category.id) == "852919409952423966"):
            await interaction.response.send_modal(SCPModal())
        else:
            await interaction.response.send_message("Канал, в якому ви знаходитесь, неможна змінювати", ephemeral=True)


class Tester(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(custom_id='persistent_view:test2', label='2', style=discord.ButtonStyle.blurple)
    async def test2(self, interaction: discord.Interaction, button:discord.Button):
        rand2 = random.randint(1, 999)
        modal = Modal(title="Вирішити тест")

        time2 = interaction.created_at
        ans2 = TextInput(label=f'Переведіть число {rand2} в 2 систему числення', required=True)
        modal.add_item(ans2)

        async def modal_submit(interaction):
            if ans2.value == in_2(rand2):
                em = discord.Embed(colour=2883328, title=f"Переведення в двійкову систему числа {rand2}",
                                   description="=======================================")
                em.add_field(name="Відповідь учасника:", value=ans2.value)
                em.add_field(name="Правильна відповідь:", value=in_2(rand2))
                em.add_field(name="Часу було витрачено", value=interaction.created_at - time2, inline=False)
                em.set_footer(text=f"Вирішував:{interaction.user.name}", icon_url=interaction.user.display_avatar)
                em.set_author(name="OK",
                              icon_url="https://cdn.pixabay.com/photo/2017/03/28/01/46/check-mark-2180770_960_720.png")
                await interaction.response.send_message(embed=em, ephemeral=True)
            else:
                em = discord.Embed(colour=16711680, title=f"Переведення в двійкову систему числа {rand2}",
                                   description="=======================================")
                em.add_field(name="Відповідь учасника:", value=ans2.value)
                em.add_field(name="Правильна відповідь:", value=in_2(rand2))
                em.add_field(name="Часу було витрачено", value=interaction.created_at - time2, inline=False)
                em.set_footer(text=f"Вирішував:{interaction.user.name}", icon_url=interaction.user.display_avatar)
                em.set_author(name="Bad",
                              icon_url="https://img1.freepng.ru/20180605/yop/kisspng-computer-icons-true-false-quiz"
                                       "-world-social-med-5b162251e0d412.6314358315281772339209.jpg")
                await interaction.response.send_message(embed=em, ephemeral=True)

        modal.on_submit = modal_submit
        await interaction.response.send_modal(modal)
        print(in_2(rand2))

    @discord.ui.button(custom_id='persistent_view:test8', label='8', style=discord.ButtonStyle.blurple)
    async def test8(self, interaction: discord.Interaction, button:discord.Button):
        rand8 = random.randint(1, 999)
        modal = Modal(title="Вирішити тест")
        time8 = interaction.created_at
        ans8 = TextInput(label=f'Переведіть число {rand8} в 8 систему числення', required=True)
        modal.add_item(ans8)

        async def modal_submit(interaction):
            if ans8.value == in_8(rand8):
                em = discord.Embed(colour=2883328, title=f"Переведення в вісімкову систему числа {rand8}",
                                   description="=======================================")
                em.add_field(name="Відповідь учасника:", value=ans8.value)
                em.add_field(name="Правильна відповідь:", value=in_8(rand8))
                em.add_field(name="Часу було витрачено", value=interaction.created_at - time8, inline=False)
                em.set_footer(text=f"Вирішував:{interaction.user.name}", icon_url=interaction.user.display_avatar)
                em.set_author(name="OK",
                              icon_url="https://cdn.pixabay.com/photo/2017/03/28/01/46/check-mark-2180770_960_720.png")
                await interaction.response.send_message(embed=em, ephemeral=True)
            else:
                em = discord.Embed(colour=16711680, title=f"Переведення в вісімкову систему числа {rand8}",
                                   description="=======================================")
                em.add_field(name="Відповідь учасника:", value=ans8.value)
                em.add_field(name="Правильна відповідь:", value=in_8(rand8))
                em.add_field(name="Часу було витрачено", value=interaction.created_at - time8, inline=False)
                em.set_footer(text=f"Вирішував:{interaction.user.name}", icon_url=interaction.user.display_avatar)
                em.set_author(name="Bad",
                              icon_url="https://img1.freepng.ru/20180605/yop/kisspng-computer-icons-true-false-quiz"
                                       "-world-social-med-5b162251e0d412.6314358315281772339209.jpg")
                await interaction.response.send_message(embed=em, ephemeral=True)

        modal.on_submit = modal_submit
        await interaction.response.send_modal(modal)
        print(in_8(rand8))

    @discord.ui.button(custom_id='persistent_view:test16', label='16', style=discord.ButtonStyle.blurple)
    async def test16(self, interaction: discord.Interaction, button:discord.Button):

        rand16 = random.randint(1, 999)
        modal = Modal(title="Вирішити тест")
        time16 = interaction.created_at
        ans16 = TextInput(label=f'Переведіть число {rand16} в 16 систему числення', required=True)
        modal.add_item(ans16)

        async def modal_submit(interaction):
            if ans16.value.upper() == in_16(rand16):
                em = discord.Embed(colour=2883328, title=f"Переведення в шістнадцяткову систему числа {rand16}",
                                   description="=======================================")
                em.add_field(name="Відповідь учасника:", value=ans16.value)
                em.add_field(name="Правильна відповідь:", value=in_16(rand16))
                em.add_field(name="Часу було витрачено", value=interaction.created_at - time16, inline=False)
                em.set_footer(text=f"Вирішував:{interaction.user.name}", icon_url=interaction.user.display_avatar)
                em.set_author(name="OK",
                              icon_url="https://cdn.pixabay.com/photo/2017/03/28/01/46/check-mark-2180770_960_720.png")
                await interaction.response.send_message(embed=em, ephemeral=True)
            else:
                em = discord.Embed(colour=16711680, title=f"Переведення в шістнадцяткову систему числа {rand16}",
                                   description="=======================================")
                em.add_field(name="Відповідь учасника:", value=ans16.value)
                em.add_field(name="Правильна відповідь:", value=in_16(rand16))
                em.add_field(name="Часу було витрачено", value=interaction.created_at - time16, inline=False)
                em.set_footer(text=f"Вирішував:{interaction.user.name}", icon_url=interaction.user.display_avatar)
                em.set_author(name="Bad",
                              icon_url="https://img1.freepng.ru/20180605/yop/kisspng-computer-icons-true-false-quiz"
                                       "-world-social-med-5b162251e0d412.6314358315281772339209.jpg")
                await interaction.response.send_message(embed=em, ephemeral=True)

        modal.on_submit = modal_submit
        await interaction.response.send_modal(modal)
        print(in_16(rand16))
