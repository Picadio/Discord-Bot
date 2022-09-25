import discord
from discord.ext import commands
from discord.ui import Modal, TextInput
import os
import random


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True

        super().__init__(command_prefix='.', intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(PersistentViewtest())
        self.add_view(PersistentView())


Bot = PersistentViewBot()


@Bot.event
async def on_ready():
    print("Bot is online")


#  MODAL


class NameModal(Modal, title="Name for channel"):
    name = TextInput(label="Name", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.user.voice.channel.edit(name=self.name.value)
        await interaction.response.send_message("")


class SCPModal(Modal, title="SET COUNT PEOPLE (0-infinity)"):
    name = TextInput(label="Count")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.user.voice.channel.edit(user_limit=int(self.name.value))
        await interaction.response.send_message("")


class PersistentView(discord.ui.View):
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


def in_2(x):
    n = []
    while x != 0:
        tmp = x % 2
        n.append(str(tmp))
        x //= 2
    n.reverse()
    q = ""
    for s in n:
        q += s
    return q


def in_8(x):
    n = []
    while x != 0:
        tmp = x % 8
        n.append(str(tmp))
        x //= 8
    n.reverse()
    q = ""
    for s in n:
        q += s
    return q


def in_16(x):
    n = []
    while x != 0:
        tmp = x % 16
        if tmp == 10:
            temp = "A"
        elif tmp == 11:
            temp = "B"
        elif tmp == 12:
            temp = "C"
        elif tmp == 13:
            temp = "D"
        elif tmp == 14:
            temp = "E"
        elif tmp == 15:
            temp = "F"
        else:
            temp = str(tmp)
        n.append(temp)
        x //= 16
    n.reverse()
    q = ""
    for s in n:
        q += s
    return q


class PersistentViewtest(discord.ui.View):
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
                              icon_url="https://img1.freepng.ru/20180605/yop/kisspng-computer-icons-true-false-quiz-world-social-med-5b162251e0d412.6314358315281772339209.jpg")
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
                              icon_url="https://img1.freepng.ru/20180605/yop/kisspng-computer-icons-true-false-quiz-world-social-med-5b162251e0d412.6314358315281772339209.jpg")
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
                              icon_url="https://img1.freepng.ru/20180605/yop/kisspng-computer-icons-true-false-quiz-world-social-med-5b162251e0d412.6314358315281772339209.jpg")
                await interaction.response.send_message(embed=em, ephemeral=True)

        modal.on_submit = modal_submit
        await interaction.response.send_modal(modal)
        print(in_16(rand16))


#    COMMAND


@Bot.command(pass_context=True)
async def id(ctx):
    await ctx.channel.send(ctx.message.author.id)


@Bot.command(pass_context=True)
async def prepare(ctx):
    if ctx.message.author.id == 343279631807545356:
        await ctx.channel.send(
            embed=discord.Embed(colour=0x39d0d6, title="Room management panel",
                                description="Name - change room name \n\n Lock - lock room \n\n Unlock - unlock room \n\n SCP - Set count people"),
            view=PersistentView()
        )
        await ctx.message.delete()


def det(n, arr):
    print(arr)
    if n == 2:
        return arr[0][0] * arr[1][1] - arr[0][1] * arr[1][0]

    ans = 0
    for i in range(n):
        arrcp = []
        for i1 in range(1, n):
            arrcp.append([arr[i1][j] for j in range(n) if (j != i)])
        ans += arr[0][i] * pow(-1, i + 1 + 1) * det(n - 1, arrcp)
        print("ANSWER")
        print(ans)
    return ans


@Bot.command(pass_context=True)
async def determinant(ctx, n_st, matrix):
    arr = []
    listt = matrix.split("\n")
    n = int(n_st)
    for a in range(n):
        arr.append([int(x) for x in listt[a].split()])
    await ctx.message.reply(det(n, arr))


@Bot.command(pass_context=True)
async def calc(ctx, message):
    await ctx.message.reply(eval(message))


@Bot.command(pass_context=True)
async def prepare_test(ctx):
    if ctx.message.author.id == 343279631807545356:
        await ctx.channel.send(
            embed=discord.Embed(colour=0x39d0d6, title="Тренувальник для переводу чисел в різні системи числення",
                                description="Оберіть в яку систему числення ви хочете переводити число"),
            view=PersistentViewtest()
        )
        await ctx.message.delete()


@Bot.command(pass_context=True)
async def in2(ctx, message):
    ms = int(message)
    ans = in_2(ms)
    await ctx.message.reply(ans)


@Bot.command(pass_context=True)
async def in8(ctx, message):
    ms = int(message)
    ans = in_8(ms)
    await ctx.message.reply(ans)

@Bot.command(pass_context=True)
async def in16(ctx, message):
    ms = int(message)
    ans = in_16(ms)
    await ctx.message.reply(ans)

@Bot.command(pass_context=True)
async def hi(ctx, message):
    await ctx.message.reply("LOL")

token = os.environ.get("BOT_TOKEN")
Bot.run(str(token))
