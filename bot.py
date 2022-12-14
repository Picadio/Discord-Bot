from discord.ext import tasks
from Class import *
import os
from discord import app_commands
import psycopg2
import datetime
import pytz
from itertools import cycle

# ====================== Constant variable ======================

UA_timezone = pytz.timezone("Europe/Kiev")
utc = (int(datetime.datetime.now(UA_timezone).strftime("%H"))-int(datetime.datetime.now().strftime("%H"))+24) % 24
status = cycle(["як написати бота", "як приготувати хом'яка"])

db_url = str(os.environ.get("DB_URL"))
db_url = db_url.replace("postgres://", "")
x = db_url.split(":")
db_user = x[0]
db_password = x[1].split("@")[0]
db_host = x[1].split("@")[1].split("/")[0]
db_name = x[1].split("/")[1]

Bot = bot()

# ====================== Members Command ======================

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


@Bot.hybrid_command(name="check_birthday_all", with_app_command=True, description="Подивитися дні народження всіх учасників")
@app_commands.guilds(discord.Object(id="1020640631175004160"))
async def check_birthday_all(ctx):
    table = psycopg2.connect(dbname=db_name, user=db_user,
                             password=db_password, host=db_host)
    cursor = table.cursor()
    cursor.execute('''SELECT * FROM birthday_tab''')
    row = cursor.fetchone()
    embed = discord.Embed(title="🎂 Дні народження 🎂", description="============================", colour=0xfff700)
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1719/1719458.png")
    embed.set_footer(text="Викликано: {0}".format(ctx.message.author.display_name), icon_url=ctx.message.author.avatar)
    while row is not None:
        user = Bot.get_guild(1020640631175004160).get_member(int(row[0]))
        md = str(row[1])
        if len(md) == 3:
            md = "0" + md
        embed.add_field(name=user.display_name, value=md[0] + md[1] + "." + md[2] + md[3] + "." + str(row[2]), inline=True)
        row = cursor.fetchone()
    await ctx.reply(embed=embed)


@Bot.hybrid_command(name="setbirthday", with_app_command=True, description="Встановити дату народження")
@app_commands.guilds(discord.Object(id="1020640631175004160"))
async def setbirthday(ctx, day, month, year):
    if len(day) == 1:
        day = "0" + day
    if len(month) == 1:
        month = "0" + month

    table = psycopg2.connect(dbname=db_name, user=db_user,
                             password=db_password, host=db_host)
    cursor = table.cursor()
    cursor.execute('''SELECT * FROM birthday_tab where id = {0}'''.format(
        str(ctx.message.author.id)))
    row = cursor.fetchone()
    if row is not None:
        cursor.execute('''UPDATE birthday_tab set month_day={0}, yr={1} where id={2}'''.format(
            day + month, int(year), str(ctx.message.author.id)))
    else:
        cursor.execute('''INSERT INTO birthday_tab (id, month_day, yr) VALUES ({0}, {1}, {2})'''.format(
            str(ctx.message.author.id), day + month, int(year)))

    table.commit()
    cursor.close()
    table.close()
    embed = discord.Embed(title="✅ Успішно", color=0x2bff00)
    embed.set_thumbnail(
        url="https://cdn-icons-png.flaticon.com/512/2362/2362432.png")
    embed.add_field(name="Дата народження", value=day + "." + month + "." + year, inline=True)
    embed.set_footer(text="Встановлено для {0}".format(ctx.message.author.name))
    await ctx.reply(embed=embed)


# ====================== Developers Commands ======================

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
    else:
        await ctx.reply("Ця команда доступна тільки розробнику")


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

@Bot.command(pass_context=True)
async def setbirthday_for(ctx, mem: discord.Member, day, month, year):
    if str(ctx.message.author.id) == "343279631807545356":
        if len(day) == 1:
            day = "0" + day
        if len(month) == 1:
            month = "0" + month
        if year == "None":
            year = "0"

        table = psycopg2.connect(dbname=db_name, user=db_user,
                                 password=db_password, host=db_host)
        cursor = table.cursor()
        cursor.execute('''SELECT * FROM birthday_tab where id = {0}'''.format(
            str(mem.id)))
        row = cursor.fetchone()
        if row is not None:
            cursor.execute(
                '''UPDATE birthday_tab set month_day={0}, yr={1} where id={2}'''.
                format(day + month, int(year), str(mem.id)))
        else:
            cursor.execute(
                '''INSERT INTO birthday_tab (id, month_day, yr) VALUES ({0}, {1}, {2})'''
                .format(str(mem.id), day + month, int(year)))
        table.commit()
        cursor.close()
        table.close()
        embed = discord.Embed(title="✅ Успішно", color=0x2bff00)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/2362/2362432.png")
        embed.add_field(name="Дата народження", value=day + "." + month + "." + year, inline=True)
        embed.set_footer(text="Встановлено для {0}".format(mem.name))
        await ctx.reply(embed=embed)
        await ctx.message.delete()
    else:
        await ctx.send("Ця команда доступна тільки розробнику")


# ====================== Auto Commands ======================

@tasks.loop(time=datetime.time(22-utc+2, 0, 0))
async def happy_birthday():
    table = psycopg2.connect(dbname=db_name,
                             user=db_user,
                             password=db_password,
                             host=db_host)
    cursor = table.cursor()
    cursor.execute('''SELECT * FROM birthday_tab where month_day={0}'''.format(
        int(datetime.datetime.now(UA_timezone).strftime("%d%m"))))
    row = cursor.fetchone()
    channel = Bot.get_guild(1020640631175004160).get_channel(1033134557467267135)
    while row is not None:
        user = Bot.get_guild(1020640631175004160).get_member(int(row[0]))
        if row[2] == '0':
            embed = discord.Embed(title="Member birthday", color=0xff00bb, description=
                "=============================== \n З ДНЕМ НАРОДЖЕННЯ {0}! 🎂 \n =============================== \n Рік народження не вказаний"
                .format(user.mention))
        else:
            embed = discord.Embed(title="Member birthday", color=0xff00bb, description=
                "=============================== \n З ДНЕМ НАРОДЖЕННЯ {0}! 🎂 \n =============================== \n Виповнилося {1}"
                .format(user.mention, datetime.datetime.now().year - int(row[2])))
        embed.set_author(name=user.name, icon_url=user.avatar)
        embed.set_thumbnail(url="https://i.imgur.com/wlA4lOm.gif")
        #embed.set_footer(text="Років виповнилося {0}".format(datetime.datetime.now().year - int(row[2])))
        #embed.add_field(name="Виповнилося", value=str(datetime.datetime.now().year - int(row[2])), inline=True)
        mess = await channel.send("@everyone")
        await channel.send(embed=embed)
        await mess.delete()
        print("Member happy " + str(user.name))
        row = tuple("0")
        row = cursor.fetchone()
    cursor.close()
    table.close()
    picadio = Bot.get_user(343279631807545356)
    await picadio.send("Happy checked")
    print("check birthday")


@tasks.loop(seconds=60)
async def change_status():
    await Bot.change_presence(activity=discord.Activity(name=next(status), type=discord.ActivityType.watching))


@Bot.event
async def on_ready():
    happy_birthday.start()
    change_status.start()
    print("Bot started at " + str(datetime.datetime.now(UA_timezone).strftime("%H:%M:%S %d.%m.%Y")))
    print(datetime.datetime.now())


token = os.environ.get("BOT_TOKEN")
Bot.run(str(token))
