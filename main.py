#import discord
import os
from discord.ext import commands
from discord.utils import get
import discord
from decouple import config

token= config('key')

client = commands.Bot(command_prefix = '!', help_command=None)

message = "Ici y a un gros pavé comme chez PlageIs"
privatemessage = "Un channel est crée à ton nom pour ton apply"

@client.event
async def on_ready():
  print(f'{client.user} has Awoken!')


@client.command()
async def apply(ctx):
  if ctx.channel.name == 'apply':
    guild = ctx.guild
    authour = ctx.message.author
  # All member who can access
    member = ctx.author
    admin_role = get(guild.roles, name="Sainte trinité")
    roster_role = get(guild.roles, name="Roster")    

  #Create new role #TODO CREATE NEW UNIQUE ROLE
    tmp = 'Candidature '+str(authour.display_name)
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

      #await ctx.send(embed=mbed)

client.run(token)
