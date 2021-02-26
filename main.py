#import discord
import os
import time
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

@client.event
async def on_ready():
  print(f'{client.user} has Awoken!')

@client.group(invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(title = "Help", description = "Use +help <command>")

  em.add_field(name = "Apply", value="Candidature")
  em.add_field(name = "Admin",value="clean,purge")
  em.add_field(name = "Other", value="ping")

  await ctx.send(embed =em)

@help.command()
async def purge(ctx):
  em = discord.Embed(title = "Purge", description= "Supprimer x messages dans le channel",color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "+purge <nombre>")
  await ctx.send(embed = em)

@help.command()
async def clean(ctx):
  em = discord.Embed(title = "Clean", description= "Permet de supprimer le channel d'un apply",color = ctx.author.color)
  em.add_field(name = "**Syntax**", value = "+clean <nom>")
  await ctx.send(embed = em)

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
      #No role continue    
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
          roster_role: discord.PermissionOverwrite(manage_messages=False,read_messages=True),
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
     await ctx.send(f'Pong! In {round(client.latency * 1000)}ms')
     await ctx.message.delete()

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
async def clean(ctx,username):
  guild = ctx.message.guild
  #Delete channel
  channelName = 'candidature-'+str(username)
  channel =  discord.utils.get(ctx.guild.channels, name=channelName)
  await channel.delete()
  ##TODO MAKE DELETE ROLE WORKING##

  #Delete role
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
        print(f'{member} à sainte trinité')
        
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


client.run(token)
