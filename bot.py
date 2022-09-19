import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from discord.ui import Button, View, Modal, TextInput
import os

class PersistentViewBot(commands.Bot):
	def __init__(self):
		intents = discord.Intents.all()
		intents.message_content = True

		super().__init__(command_prefix='.', intents=intents)

	async def setup_hook(self) -> None:
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

token = os.environ.get("BOT_TOKEN")
Bot.run(str(token))
