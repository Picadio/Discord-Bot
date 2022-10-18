from Class import *
import os
from discord import app_commands

Bot = bot()


@Bot.event
async def on_ready():
    print("Bot is online")

#    COMMAND


@Bot.command(pass_context=True)
async def prepare(ctx, message):
    if ctx.message.author.id == 343279631807545356:
        if message == "0":
            await ctx.channel.send(
                embed=discord.Embed(colour=0x39d0d6, title="Room management panel",
                                    description="Name - change room name \n\n Lock - lock room \n\n Unlock - unlock "
                                                "room \n\n SCP - Set count people"),
                view=ControlPanel()
            )
            await ctx.message.delete()
        if message == "1":
            await ctx.channel.send(
                embed=discord.Embed(colour=0x39d0d6, title="Тренувальник для переводу чисел в різні системи числення",
                                    description="Оберіть в яку систему числення ви хочете переводити число"),
                view=Tester()
            )
            await ctx.message.delete()


@Bot.command(pass_context=True)
async def determinant(ctx, size, *, matrix):
    arr = []
    listt = matrix.split("\n")
    n = int(size)
    for a in range(n):
        arr.append([float(x) for x in listt[a].split()])
    await ctx.defer()
    await ctx.reply(det(n, arr))


@Bot.hybrid_command(name="in2", with_app_command=True, description="Перевести число в двійкову систему числення")
@app_commands.guilds(discord.Object(id="1020640631175004160"))
async def reformat(ctx, x, input_type, output_type):
    await ctx.defer(ephemeral=True)
    await ctx.reply(reform(x, input_type, output_type))



@Bot.hybrid_command(name="add2", with_app_command=True, description="Додати числа в двійковій системі")
@app_commands.guilds(discord.Object(id="1020640631175004160"))
async def add2(ctx, num_1, num_2, input_type):
    if input_type == "10":
        num_1 = in_2(int(num_1))
        num_2 = in_2(int(num_2))

    ans = add2(num_1, num_2)
    await ctx.defer(ephemeral=True)
    await ctx.reply(num_1, "\n +", num_2, "\n", ans)


token = os.environ.get("BOT_TOKEN")
Bot.run(str(token))