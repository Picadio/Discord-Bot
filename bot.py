import asyncio
import datetime

import discord

from Class import *
import os
from discord import app_commands
import psycopg2
from threading import Thread
from time import sleep

db_url = str(os.environ.get("DATABASE_URL"))
db_url = db_url.replace("postgres://", "")
x = db_url.split(":")
db_user = x[0]
db_password = x[1].split("@")[0]
db_host = x[1].split("@")[1]
db_name = x[2].split("/")[1]

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


@Bot.hybrid_command(name="reformat", with_app_command=True, description="Перевести число із будь-якої системи числення в будь-яку.")
@app_commands.guilds(discord.Object(id="1020640631175004160"))
async def reformat(ctx, x, input_type, output_type):
    ans = reform(x, input_type, output_type)
    print("reformat func:", ctx.message.author, x, ans)
    await ctx.defer(ephemeral=True)
    await ctx.reply(ans)


@Bot.hybrid_command(name="setbirthday", with_app_command=True, description="Встановити дату народження")
@app_commands.guilds(discord.Object(id="1020640631175004160"))
async def setbirthday(ctx, day, month, year):
    table = psycopg2.connect(dbname=db_name, user=db_user,
                             password=db_password, host=db_host)
    cursor = table.cursor()
    cursor.execute('''SELECT * FROM birthday_tab where id = {0}'''.format(str(ctx.message.author.id)))
    row = cursor.fetchone()
    if row is not None:
        cursor.execute('''UPDATE birthday_tab set month_day={0}, yr={1} where id={2}'''.format(day+month, int(year), str(ctx.message.author.id)))
    else:
        cursor.execute('''INSERT INTO birthday_tab (id, month_day, yr) VALUES ({0}, {1}, {2})'''.format(str(ctx.message.author.id), day+month, int(year)))
    table.commit()
    cursor.close()
    table.close()
    embed = discord.Embed(title="✅ Успішно", color=0x2bff00)
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/2362/2362432.png")
    embed.add_field(name="Дата народження", value=day+"."+month+"."+year, inline=True)
    embed.set_footer(text="Встановлено для {0}".format(ctx.message.author))
    await ctx.reply(embed=embed)



@Bot.command(pass_context=True)
async def crtable(ctx):
    if str(ctx.message.author.id) == "343279631807545356":

        table = psycopg2.connect(dbname=db_name, user=db_user,
                                password=db_password, host=db_host)

        cursor = table.cursor()
        cursor.execute('''CREATE TABLE birthday_tab (id bigint, month_day integer, yr integer)''')
        table.commit()
        print("Sucessful")
        cursor.close()
        table.close()

    else:
        await ctx.reply("Ця команда доступна тільки розробнику")


def congrat_happy_birthday():
    channel = discord.TextChannel
    table = psycopg2.connect(dbname=db_name, user=db_user,
                             password=db_password, host=db_host)
    cursor = table.cursor()
    cursor.execute('''SELECT * FROM birthday_tab where month_day={0}'''.format(datetime.datetime.now().strftime("%d%m")))
    row = cursor.fetchone()
    for i in Bot.guilds:
        if channel == discord.TextChannel:
            for j in i.text_channels:
                print(j.id)
                if str(j.id) == "1033134557467267135":
                    print("da")
                    print(j.name)
                    channel = j
                    break
        else:
            break
    print(channel.name)
    while row is not None:
        for i in Bot.guilds:
            for j in i.members:
                if str(j.id) == str(row[0]):
                    embed = discord.Embed(title="<big><b>Member birthday</b></big>", color=0x2bff00)
                    embed.set_author(name=j.name, icon_url=j.display_icon)
                    embed.set_thumbnail(url="https://i.imgur.com/wlA4lOm.gif")
                    embed.add_field(name="", value="З ДНЕМ НАРОДЖЕННЯ {0}! 🎂".format(j.mention), inline=True)
                    channel.send(embed=embed)
                    print("Member happy"+str(j.id))
                    break
        row = cursor.fetchone()
    print("CONGRAT DONE")
    cursor.close()
    table.close()


def happy_birthday():
    while True:
        if int(datetime.datetime.now().strftime("%H"))+3 == 20:
            print("congrat")
            congrat_happy_birthday()
        print("plak")
        sleep(60)


Thread(target=happy_birthday).start()

token = os.environ.get("BOT_TOKEN")
Bot.run(str(token))
