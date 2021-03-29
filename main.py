#import discord
import os
import time
import requests
import json
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from discord.utils import get
import discord
from decouple import config

token= config('key')

client = commands.Bot(command_prefix = '+')
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
msg = None


@client.event
async def on_ready():
  #print('{client.user} has Awoken!')
  print("{} has awoken !".format(client.user))
@client.group(invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(title = "Help", description = "Use +help <command>")

  em.add_field(name = "Apply", value="Candidature")
  em.add_field(name = "Admin",value="clean,purge,mute,unmute,reaction, participant,closevote")
  em.add_field(name = "All", value="ping,raiderio")

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
          roster_role: discord.PermissionOverwrite(manage_messages=False,read_messages=True,send_messages=False),
          authour_role: discord.PermissionOverwrite(read_messages=True)
        }

        #Create channel
        nameChannel="candidature "+str(ctx.author.display_name)
        await guild.create_text_channel(name=nameChannel,overwrites=overwrites)
        #Send Private Message
        await ctx.author.send(privatemessage)    
    await ctx.message.delete()

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
  #Delete channel
  channelName = 'candidature-'+str(username)
  channel =  discord.utils.get(ctx.guild.channels, name=channelName)
  await channel.delete()
  ##TODO MAKE DELETE ROLE WORKING##

  # Delete role
  #roleName='Candidature '+str(username)
  #print(f'-----------------------------------------')
  #role = discord.utils.get(ctx.message.roles, name=roleName)
  #print(f'*****************************************')
  #await client.remove_roles(role)

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

@client.event
async def on_reaction_add(reaction, user):
  if reaction.message == msg:
    people_list.append(user)

@client.command(pass_context=True)
@has_permissions(administrator=True)
async def participant(ctx):
  await ctx.channel.purge(limit=1)
  await ctx.send("**Personnes qui ont cliqué sur '✅' :**")
  temp = ""
  for i in range(len(people_list)):
    if i != 0:
      temp+=("{}\n".format(people_list[i].nick))
      #await ctx.send("{}".format(people_list[i].nick))
  await ctx.send(temp)

@client.command(pass_context=True)
@has_permissions(administrator=True)
async def closevote(ctx):
  await ctx.channel.purge(limit=1)
  await ctx.send("**Vote fini, les personnes qui ont cliqué sur '✅' sont :**")
  for i in range(len(people_list)):
    if i != 0:
      await ctx.send("{}".format(people_list[i].nick))
  global msg 
  global people_list
  msg = None
  people_list = []


client.run(token)
