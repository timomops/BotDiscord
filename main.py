#import discord
import os
import glob
import time
import requests
import json
import string
import random
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from discord.utils import get
import discord
from decouple import config
from datetime import datetime

intents = discord.Intents.all()

token= config('key')

client = commands.Bot(command_prefix = '+',intents=intents)
client.remove_command("help")

privatemessage = """Candidature - Clarity
1)Qui es-tu ?
Fais nous un petit topo sur qui tu es, quel âge as-tu ...

2) Que joues-tu ?
Explique nous quelle classe, quelle spé, ton optimisation, pourquoi ces choix?
3) Des informations complémentaires : 
Un Screen de ton interface, un lien vers ton Warcraftlogs, un Lien de ton dps sur raidbot, toute info qui te semble pertinente."""

alreadyapply = "Un channel existe déja pour ton apply"

people_list = []
refuse_list = []
msg = None

year=[]
month=[]
day=[]

id_channel_mp_bot = 862835138760278086
path_patch = "patch/date.txt"

@client.event
async def on_ready():
  #print('{client.user} has Awoken!')
  print("{} has awoken !".format(client.user))
@client.group(invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(title = "Help", description = "Use +help <command>")

  em.add_field(name = "Apply", value="Candidature")
  em.add_field(name = "Admin",value="clean,purge,reaction,participant,closevote,strawpoll,closestrawpoll")
  em.add_field(name = "All", value="ping,raiderio,roll")

  await ctx.send(embed =em)

@help.command()
async def purge(ctx):
  em = discord.Embed(title = "Purge", description= "Supprimer x messages dans le channel",color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "+purge <nombre>")
  await ctx.send(embed = em)

@help.command()
async def raiderio(ctx):
  em = discord.Embed(title = "Raiderio", description= "Chercher le raiderIo d'une personne",color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "+raiderio <region> <realm> <username>\n Exemple : +raiderio eu archimonde phanttømax")
  await ctx.send(embed = em)

@help.command()
async def clean(ctx):
  em = discord.Embed(title = "Clean", description= "Permet de supprimer le channel d'un apply",color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "+clean <nom>")
  await ctx.send(embed = em)

@help.command()
async def mute(ctx):
  em = discord.Embed(title = "Mute", description= "Mute tout les membres dans le channel vocal sauf la Sainte trinité",color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "+mute")
  await ctx.send(embed = em)

@help.command()
async def unmute(ctx):
  em = discord.Embed(title = "Unmute", description= "Unmute tout les membres dans le channel vocal",color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "+unmute")
  await ctx.send(embed = em)

@help.command()
async def reaction(ctx):
  em = discord.Embed(title = "reaction", description= "Créer un message permettant aux utilisateurs de voter",color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "+reaction")
  await ctx.send(embed = em)

@help.command()
async def participant(ctx):
  em = discord.Embed(title = "reaction", description= "Permet d'envoyer la liste des personnes ayant voté",color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "+participant")
  await ctx.send(embed = em)

@help.command()
async def closevote(ctx):
  em = discord.Embed(title = "reaction", description= "Ferme le vote et envoie la liste des personnes ayant voté",color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "+closevote")
  await ctx.send(embed = em)

@help.command()
async def roll(ctx):
  em = discord.Embed(title = "roll", description= "Fais un roll entre le premier et le deuxième chiffre",color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "+roll")
  await ctx.send(embed = em)


#### Seperate help command with command bot ####

#Apply clarity
@client.command()
async def Candidature(ctx):
  if ctx.channel.name == 'apply':
    guild = ctx.guild
    authour = ctx.message.author
    checkRole = discord.utils.get(ctx.guild.roles, name="Roster")
    idiot="Idiot du village"
    if checkRole in ctx.author.roles:
      #Already has a role
      await ctx.author.send('Tu as déjà un rôle idiot !')
      if get(ctx.guild.roles, name=idiot):
        idiotRole = discord.utils.get(ctx.guild.roles, name=idiot)
        await authour.add_roles(idiotRole)
      else:
        idiotRole = await guild.create_role(name=idiot,permissions=discord.Permissions(3072),reason="Un idiot est née")
        await authour.add_roles(idiotRole)
    else:
      #No role continu
      #All member who can access
      member = ctx.author
      admin_role = get(guild.roles, name="Sainte trinité")
      apply_manager_role = get(guild.roles, name="Public Relations Manager")
      roster_role = get(guild.roles, name="Roster")
      tmp = 'Candidature '+str(authour.display_name)

      #Create new role
      if get(ctx.guild.roles,name=tmp):  
        await ctx.author.send(alreadyapply)
      else:
        #Create role with permissions Read / Send messages / Embed link / History / View channel
        role = await guild.create_role(name=tmp, permissions=discord.Permissions(84992),reason= 'new_apply')
        await authour.add_roles(role)
        authour_role = get(guild.roles,name=str(tmp))
        #List of permissions
        overwrites = {
          guild.default_role: discord.PermissionOverwrite(read_messages=False),
          guild.me: discord.PermissionOverwrite(read_messages=True),
          admin_role: discord.PermissionOverwrite(read_messages=True),
          apply_manager_role: discord.PermissionOverwrite(read_messages=True,manage_messages=False,send_messages=True),
          roster_role: discord.PermissionOverwrite(manage_messages=False,read_messages=True,send_messages=False),
          authour_role: discord.PermissionOverwrite(read_messages=True)
        }

        #Create channel
        nameChannel="candidature "+str(ctx.author.display_name)
        await guild.create_text_channel(name=nameChannel,overwrites=overwrites)
        #Send Private Message
        await ctx.author.send(privatemessage)    
    await ctx.message.delete()

#Respond to private message
@client.event
async def on_message(message):
  if message.author.id != client.user.id:
    if message.guild:  # If message in guild
      await client.process_commands(message)  # Process command
    else:
      print(" Débile : {0.author.name} à mp le bot pour dire : {0.content}".format(message))
      text = str(message.author.name) + " mp : " +str(message.content)
      channel = client.get_channel(id_channel_mp_bot)
      await channel.send(text)
      return await message.author.send("Merci de relire l'étape 1 dans le channel **apply**")

@client.command()
async def Createchannel(ctx):
  guild = ctx.guild
  os.chdir("mydir")
  #List of permissions
  admin_role = get(guild.roles, name="Sainte trinité")
  roster_role = get(guild.roles, name="Roster")
  overwrites = {
    guild.default_role: discord.PermissionOverwrite(read_messages=False),
    guild.me: discord.PermissionOverwrite(read_messages=True),
    admin_role: discord.PermissionOverwrite(read_messages=True),
    roster_role: discord.PermissionOverwrite(manage_messages=False,read_messages=True,send_messages=False)
  }  
  for file in glob.glob("*"):
    #Get filename
    nameChannel = str(file.split('.')[0])
    await guild.create_text_channel(name=nameChannel,overwrites=overwrites)
  await ctx.message.delete()


## -------------------------------------------------------------------###

#Track people who leave discord
@client.event
async def on_member_remove(member):
  channel = client.get_channel(id_channel_mp_bot)
  text = str(member) + " has left the server"
  await channel.send(text)


## -------------------------------------------------------------------###

#Ping bot
@client.command()
async def ping(ctx):
  await ctx.send('Pong! In {round(client.latency * 1000)}ms')
  await ctx.message.delete()

#Check raider.io 
@client.command()
async def raiderio(ctx,region,realm,name):
	#https://raider.io/api/
	parameters = {'region': region, 'realm':realm,'name': name}
	response = requests.get(url="https://raider.io/api/v1/characters/profile", params=parameters)
	data = response.json()
	await ctx.send(data['profile_url'])

#Purge x message
@client.command(pass_context=True)
async def purge(ctx, limit: int):
  guild= ctx.message.guild
  checkRole = discord.utils.get(ctx.guild.roles, name="Sainte trinité")
  if checkRole in ctx.author.roles:
    await ctx.message.delete()
    await ctx.channel.purge(limit=limit)
  else:
    msg = "Non, je crois pas : {}".format(ctx.message.author.mention)
    await ctx.send(msg)

#Clean channel apply
@client.command()
@commands.has_permissions(administrator = True)
async def clean(ctx,username):
  guild = ctx.message.guild
  #Copy discution in the channel to files
  await ctx.message.delete()
  filename=username+".txt"
  with open(filename, "w") as f:
    async for message in ctx.history(limit=1000):
      f.write(message.author.name + " : " + message.content + "\n")

  #Delete channel
  channelName = 'candidature-'+str(username)
  channel =  discord.utils.get(ctx.guild.channels, name=channelName)
  await channel.delete()
  #Delete role
  roleName="Candidature "+str(username)
  #print("roleName : ", roleName)
  role_object = discord.utils.get(ctx.message.guild.roles, name=roleName)
  if role_object:
      await role_object.delete()
  else:
    roleName = string.capwords(roleName)
    role_object = discord.utils.get(ctx.message.guild.roles, name=roleName)
    await role_object.delete()

#Roll the dice
@client.command()
async def roll(ctx,number_1, number_2):
  n = random.randint(int(number_1),int(number_2))
  message = "Tu as fait un " + str(n) + " !"
  await ctx.send(message)

#Mute all except Sainte trinité
@client.command()
async def mute(ctx):
  vc = ctx.author.voice.channel
  for member in vc.members:
    tmp = 0
    #List
    for role in member.roles:
      if ('Sainte trinité' in str(role)):
        tmp = 1
        #print(f'{member} à sainte trinité')
        
    if tmp != 0:
      await member.edit(mute=False)
    else:
      await member.edit(mute=True)    

#Unmute all
@client.command()
async def unmute(ctx):
  vc = ctx.author.voice.channel
  guild= ctx.message.guild
  for member in vc.members:
    await member.edit(mute=False)

@client.command(pass_context=True)
@has_permissions(administrator=True)
async def reaction(ctx):
  await ctx.channel.purge(limit=1)
  global msg
  msg = await ctx.send("**Clique sur '✅' si tu participes au post précedent!**")
  reactions = ['✅']
  for emoji in reactions:
    await msg.add_reaction(emoji)

@client.command(pass_context=True)
@has_permissions(administrator=True)
async def strawpoll(ctx):
  await ctx.channel.purge(limit=1)
  global msg
  msg = await ctx.send("**Vote '✅' ou '❎'**")
  reactions = ['✅','❎']
  for emoji in reactions:
    await msg.add_reaction(emoji)

@client.event
async def on_reaction_add(reaction, user):
  if reaction.message == msg:
    if str(reaction) == "✅" :
      if user in people_list:
        pass
      else:
        people_list.append(user)
    else:
      if user in refuse_list:
        pass
      else:
        refuse_list.append(user)
    #print(user)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if user.nick == None:
      print(user,"à",dt_string,"vote :",reaction)
    else:
      print(user.nick,"à", dt_string,"vote :",reaction)

@client.command(pass_context=True)
@has_permissions(administrator=True)
async def participant(ctx):
  await ctx.channel.purge(limit=1)
  await ctx.send("**Personnes qui ont cliqué sur '✅' :**")
  temp = ""
  #print("{}".format(people_list))
  for i in range(len(people_list)):
    if i != 0:
      if people_list[i].nick == None:
        #print("{}\n".format(people_list[i]))
        temp+=("{}\n".format(people_list[i].name))
      else:
        temp+=("{}\n".format(people_list[i].nick))
      #await ctx.send("{}".format(people_list[i].nick))
  if temp == "":
    temp = "Personne"
  await ctx.send(temp)
  await ctx.send("**Personnes qui ont cliqué sur '❎' :**")
  temp = ""
  for i in range(len(refuse_list)):
    if i != 0:
      if refuse_list[i].nick == None:
        #print("{}\n".format(refuse_list[i]))
        temp+=("{}\n".format(refuse_list[i].name))
      else:
        temp+=("{}\n".format(refuse_list[i].nick))
      #await ctx.send("{}".format(refuse_list[i].nick))
  if temp == "":
    temp = "Personne"
  await ctx.send(temp)

@client.command(pass_context=True)
@has_permissions(administrator=True)
async def closevote(ctx):
  global msg 
  global people_list
  await ctx.channel.purge(limit=1)
  await ctx.send("**Vote fini, les personnes qui ont cliqué sur '✅' sont :**")
  temp = ""
  for i in range(len(people_list)):
    if i != 0:
      if people_list[i].nick == None:
        #print("{}\n".format(people_list[i]))
        temp+=("{}\n".format(people_list[i].name))
      else:
        temp+=("{}\n".format(people_list[i].nick))
  if temp == "":
    temp = "Personne"
  await ctx.send(temp)
  msg = None
  people_list = []

@client.command(pass_context=True)
@has_permissions(administrator=True)
async def closestrawpoll(ctx):
  global msg 
  global people_list
  global refuse_list
  await ctx.channel.purge(limit=1)
  await ctx.send("**Vote fini, les personnes qui ont cliqué sur '✅' sont :**")
  temp = ""
  for i in range(len(people_list)):
    if i != 0:
      if people_list[i].nick == None:
        #print("{}\n".format(people_list[i]))
        temp+=("{}\n".format(people_list[i].name))
      else:
        temp+=("{}\n".format(people_list[i].nick))
      #await ctx.send("{}".format(people_list[i].nick))
  if temp == "":
    temp = "Personne"
  await ctx.send(temp)
  await ctx.send("**Et les personnes qui ont cliqué sur '❎' sont :**")
  temp = ""
  for i in range(len(refuse_list)):
    if i != 0:
      if refuse_list[i].nick == None:
        #print("{}\n".format(refuse_list[i]))
        temp+=("{}\n".format(refuse_list[i].name))
      else:
        temp+=("{}\n".format(refuse_list[i].nick))
      #await ctx.send("{}".format(refuse_list[i].nick))
  if temp == "":
    temp = "Personne"
  await ctx.send(temp)  
  msg = None
  people_list = []
  refuse_list = []


@client.command(pass_context=True)
async def lastpatch(ctx):
  #read file and parse
  file = open(path_patch)
  with open(path_patch) as f:
    content = f.readlines()
    for i in range(len(content)):
      tmp = str(content[i]).split('=')[1]
      year.append(tmp.split('-')[0])
      month.append(tmp.split('-')[1])
      day.append(tmp.split('-')[2])

  #calcul and send
  last_patch = datetime(int(year[0]), int(month[0]), int(day[0]))
  now  = datetime.now()
  duration = now - last_patch
  duration_in_s = duration.total_seconds()

  days  = duration.days
  days  = divmod(duration_in_s, 86400)[0]  
  days = int(days)
  send = "Le dernier patch était il y a " +str(days) +" jours"
  await ctx.send(send)
  #Clean variable and close file 
  file.close()
  f.close()
  year.clear()
  month.clear()
  day.clear()

client.run(token)
