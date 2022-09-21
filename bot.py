import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from discord.ui import Button, View, Modal, TextInput
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


'''MODAL'''
class NameModal(Modal, title="Name for channel"):
	TIname = TextInput(label="Name", required=True)
	async def on_submit(self, interaction: discord.Interaction):
		await interaction.user.voice.channel.edit(name=self.TIname.value)
		await interaction.response.send_message("")

class SCPModal(Modal, title="SET COUNT PEOPLE (0-infinity)"):
	TIname = TextInput(label="Count")

	async def on_submit(self, interaction: discord.Interaction):
		await interaction.user.voice.channel.edit(user_limit=int(self.TIname.value))
		await interaction.response.send_message("")



class PersistentView(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)

	@discord.ui.button(custom_id='persistent_view:name_bt', label='Name', style=discord.ButtonStyle.blurple)
	async def name_bt(self, interaction: discord.Interaction, button: discord.ui.Button):
		if (interaction.user.voice==None):
			await interaction.response.send_message("Ви не знаходитесь у голосовому каналі", ephemeral=True)
		elif(interaction.user.voice.channel.category.name=="🔒 CREATE Private channels"):
			await interaction.response.send_modal(NameModal())
		else:
			await interaction.response.send_message("Канал, в якому ви знаходитесь, неможна змінювати", ephemeral=True)

	@discord.ui.button(custom_id='persistent_view:lock_bt', label='Lock', style=discord.ButtonStyle.blurple)
	async def lock_bt(self, interaction: discord.Interaction, button: discord.ui.Button):
		role = interaction.guild.default_role
		if (interaction.user.voice==None):
			await interaction.response.send_message("Ви не знаходитесь у голосовому каналі", ephemeral=True)
		elif(interaction.user.voice.channel.category.name=="🔒 CREATE Private channels"):
			await interaction.user.voice.channel.set_permissions(role, connect=False)
			await interaction.response.send_message(" ")
		else:
			await interaction.response.send_message("Канал, в якому ви знаходитесь, неможна змінювати", ephemeral=True)

	@discord.ui.button(custom_id='persistent_view:unlock_bt', label='Unlock', style=discord.ButtonStyle.blurple)
	async def unlock_bt(self, interaction: discord.Interaction, button: discord.ui.Button):
		role = interaction.guild.default_role
		if (interaction.user.voice==None):
			await interaction.response.send_message("Ви не знаходитесь у голосовому каналі", ephemeral=True)
		elif(interaction.user.voice.channel.category.name=="🔒 CREATE Private channels"):
			await interaction.user.voice.channel.set_permissions(role, connect=True)
			await interaction.response.send_message(" ")
		else:
			await interaction.response.send_message("Канал, в якому ви знаходитесь, неможна змінювати", ephemeral=True)

	@discord.ui.button(custom_id='persistent_view:scp_bt', label='SCP', style=discord.ButtonStyle.blurple)
	async def scp_bt(self, interaction: discord.Interaction, button: discord.ui.Button):
		if (interaction.user.voice==None):
			await interaction.response.send_message("Ви не знаходитесь у голосовому каналі", ephemeral=True)
		elif(interaction.user.voice.channel.category.name=="🔒 CREATE Private channels"):
			await interaction.response.send_modal(SCPModal())
		else:
			await interaction.response.send_message("Канал, в якому ви знаходитесь, неможна змінювати", ephemeral=True)

def in_2(x):
	list = []
	while x!=0:
		tmp=x%2
		list.append(str(tmp))
		x//=2
	list.reverse()
	q = ""
	for s in list:
		q+=s
	return q



class twomodal(Modal, title="Вирішити тест"):
	async def on_submit(self, interaction: discord.Interaction):
		global ans
		global rand
		global time
		if(ans.value == in_2(rand)):
			em = discord.Embed(colour= 2883328, title=f"Переведення в двійкову систему числа {rand}", description="=======================================")
			em.add_field(name="Відповідь учасника:", value=ans.value)
			em.add_field(name="Правильна відповідь:", value=in_2(rand))
			em.add_field(name="Часу було витрачено", value=interaction.created_at-time, inline=False)
			em.set_footer(text=f"Вирішував:{interaction.user.name}", icon_url=interaction.user.display_avatar)
			em.set_author(name="OK", icon_url="https://cdn.pixabay.com/photo/2017/03/28/01/46/check-mark-2180770_960_720.png")
			await interaction.response.send_message(embed=em, ephemeral=True)
		else:
			em = discord.Embed(colour= 16711680, title=f"Переведення в двійкову систему числа {rand}", description="=======================================")
			em.add_field(name="Відповідь учасника:", value=ans.value)
			em.add_field(name="Правильна відповідь:", value=in_2(rand))
			em.add_field(name="Часу було витрачено", value=interaction.created_at-time, inline=False)
			em.set_footer(text=f"Вирішував:{interaction.user.name}", icon_url=interaction.user.display_avatar)
			em.set_author(name="Bad", icon_url="https://img1.freepng.ru/20180605/yop/kisspng-computer-icons-true-false-quiz-world-social-med-5b162251e0d412.6314358315281772339209.jpg")
			await interaction.response.send_message(embed=em, ephemeral=True)

def in_8(x):
	list = []
	while x!=0:
		tmp=x%8
		list.append(str(tmp))
		x//=8
	list.reverse()
	q = ""
	for s in list:
		q+=s
	return q

class eightmodal(Modal, title="Вирішити тест"):
	async def on_submit(self, interaction: discord.Interaction):
		global ans
		global rand
		global time
		if(ans.value == in_8(rand)):
			em = discord.Embed(colour= 2883328, title=f"Переведення в вісімкову систему числа {rand}", description="=======================================")
			em.add_field(name="Відповідь учасника:", value=ans.value)
			em.add_field(name="Правильна відповідь:", value=in_8(rand))
			em.add_field(name="Часу було витрачено", value=interaction.created_at-time, inline=False)
			em.set_footer(text=f"Вирішував:{interaction.user.name}", icon_url=interaction.user.display_avatar)
			em.set_author(name="OK", icon_url="https://cdn.pixabay.com/photo/2017/03/28/01/46/check-mark-2180770_960_720.png")
			await interaction.response.send_message(embed=em, ephemeral=True)
		else:
			em = discord.Embed(colour= 16711680, title=f"Переведення в вісімкову систему числа {rand}", description="=======================================")
			em.add_field(name="Відповідь учасника:", value=ans.value)
			em.add_field(name="Правильна відповідь:", value=in_8(rand))
			em.add_field(name="Часу було витрачено", value=interaction.created_at-time, inline=False)
			em.set_footer(text=f"Вирішував:{interaction.user.name}", icon_url=interaction.user.display_avatar)
			em.set_author(name="Bad", icon_url="https://img1.freepng.ru/20180605/yop/kisspng-computer-icons-true-false-quiz-world-social-med-5b162251e0d412.6314358315281772339209.jpg")
			await interaction.response.send_message(embed=em, ephemeral=True)

def in_16(x):
	list = []
	while x!=0:
		tmp=x%16
		if(tmp==10):
			temp="a"
		elif(tmp==11):
			temp="b"
		elif(tmp==12):
			temp="c"
		elif(tmp==13):
			temp="d"
		elif(tmp==14):
			temp="e"
		elif(tmp==15):
			temp="f"
		else:
			temp = str(tmp)
		list.append(temp)
		x//=16
	list.reverse()
	q = ""
	for s in list:
		q+=s
	return q

class sixteenmodal(Modal, title="Вирішити тест"):
	async def on_submit(self, interaction: discord.Interaction):
		global ans
		global rand
		global time
		if(ans.value.lower() == in_16(rand)):
			em = discord.Embed(colour= 2883328, title=f"Переведення в шістнадцяткову систему числа {rand}", description="=======================================")
			em.add_field(name="Відповідь учасника:", value=ans.value)
			em.add_field(name="Правильна відповідь:", value=in_16(rand))
			em.add_field(name="Часу було витрачено", value=interaction.created_at-time, inline=False)
			em.set_footer(text=f"Вирішував:{interaction.user.name}", icon_url=interaction.user.display_avatar)
			em.set_author(name="OK", icon_url="https://cdn.pixabay.com/photo/2017/03/28/01/46/check-mark-2180770_960_720.png")
			await interaction.response.send_message(embed=em, ephemeral=True)
		else:
			em = discord.Embed(colour= 16711680, title=f"Переведення в шістнадцяткову систему числа {rand}", description="=======================================")
			em.add_field(name="Відповідь учасника:", value=ans.value)
			em.add_field(name="Правильна відповідь:", value=in_16(rand))
			em.add_field(name="Часу було витрачено", value=interaction.created_at-time, inline=False)
			em.set_footer(text=f"Вирішував:{interaction.user.name}", icon_url=interaction.user.display_avatar)
			em.set_author(name="Bad", icon_url="https://img1.freepng.ru/20180605/yop/kisspng-computer-icons-true-false-quiz-world-social-med-5b162251e0d412.6314358315281772339209.jpg")
			await interaction.response.send_message(embed=em, ephemeral=True)

class PersistentViewtest(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)

	@discord.ui.button(custom_id='persistent_view:test2', label='2', style=discord.ButtonStyle.blurple)
	async def test2(self, interaction: discord.Interaction, button: discord.ui.Button):
			global rand
			rand = random.randint(1, 100)
			modal = twomodal()
			global ans
			global time
			time = interaction.created_at
			ans = TextInput(label=f'Перведіть число {rand} в 2 систему числення', required=True)
			modal.add_item(ans)

			await interaction.response.send_modal(modal)
			print(in_2(rand))
	@discord.ui.button(custom_id='persistent_view:test8', label='8', style=discord.ButtonStyle.blurple)
	async def test8(self, interaction: discord.Interaction, button: discord.ui.Button):
		global rand
		rand = random.randint(1, 100)
		modal = eightmodal()
		global ans
		global time
		time = interaction.created_at
		ans = TextInput(label=f'Перведіть число {rand} в 8 систему числення', required=True)
		modal.add_item(ans)

		await interaction.response.send_modal(modal)
		print(in_8(rand))
	@discord.ui.button(custom_id='persistent_view:test16', label='16', style=discord.ButtonStyle.blurple)
	async def test16(self, interaction: discord.Interaction, button: discord.ui.Button):
		global rand
		rand = random.randint(1, 100)
		modal = sixteenmodal()
		global ans
		global time
		time = interaction.created_at
		ans = TextInput(label=f'Перведіть число {rand} в 16 систему числення', required=True)
		modal.add_item(ans)

		await interaction.response.send_modal(modal)
		print(in_16(rand))

"""COMMAND"""


@Bot.command(pass_context=True)
async def id(ctx):
	await ctx.channel.send(ctx.message.author.id)

@Bot.command(pass_context=True)
async def prepare(ctx):
	if(ctx.message.author.id == 343279631807545356 and ctx.message.channel.name == "commands"):
		await ctx.channel.send(
		embed=discord.Embed(colour= 0x39d0d6,title="Room management panel", description="Name - change room name \n\n Lock - lock room \n\n Unlock - unlock room \n\n SCP - Set count people"),
		view=PersistentView()	
		)
		await ctx.message.delete()
def det(n, arr):
	print(arr)
	if(n==2):
		return arr[0][0]*arr[1][1]-arr[0][1]*arr[1][0]
	
	ans=0
	for i in range(n):
		arrcp=[]
		for i1 in range(1, n):
			arrcp.append([arr[i1][j] for j in range(n) if(j!=i) ])
		ans+=arr[0][i]*pow(-1, i+1+1)*det(n-1, arrcp)
		print("ANSWER")
		print (ans)
	return ans

@Bot.command(pass_context=True)
async def determinant(ctx, n_st, matrix):
	arr=[]
	listt = matrix.split("\n")
	n=int(n_st)
	for a in range(n):	
		arr.append([int(x) for x in listt[a].split()])
	await ctx.message.reply(det(n, arr))

@Bot.command(pass_context=True)
async def calc(ctx, message):
	await ctx.message.reply(eval(message))
	
@Bot.command(pass_context=True)
async def prepare_test(ctx):
	if(ctx.message.author.id == 343279631807545356):
		await ctx.channel.send(
			embed=discord.Embed(colour= 0x39d0d6,title="Тренувальник для переводу чисел в різні систми числення",description="Оберіть в яку систему числення ви хочете переводити число"),
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

token = os.environ.get("BOT_TOKEN")
Bot.run(str(token))
