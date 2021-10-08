import asyncio
import traceback

import discord
import requests
import discord.ext
from discord.ext import commands
import Time
import main2
import Data_base
from pygicord import Paginator
import os

client = commands.Bot(command_prefix='%', help_command=None)

text_channel_list = []
upcoming_data = []
default_data = [
    'codeforces.com', 'codechef.com', 'atcoder.jp',
    'codingcompetitions.withgoogle.com'
]
db = Data_base.data_base()
supported_data = [
    'codeforces.com', 'codechef.com', 'atcoder.jp', 'hackerearth.com',
    'codingcompetitions.withgoogle.com', 'ctftime.org', 'russianaicup.ru',
    'dl.gsu.by', 'e-olymp.com', 'neerc.ifmo.ru/trains', 'topcoder.com',
    'algorithm.contest.yandex.com', 'battlecode.org', 'ch24.org',
    'leetcode.com', 'csacademy.com'
]


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            'Missing the required arguments \n check out %help for more details on commands'
        )
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send(
            'Too many arguments/n check out %help for more details on commands'
        )
    else:
        f = open("errors.txt", "a")
        f.write(f'{error}')
        f.close()


async def check(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            global text_channel_list
            text_channel_list.append(channel)
            return channel


def print_website(temp):
    s = ''
    for website in temp:
        s += f'{website}\n'
    embed = discord.Embed(title=' Your Subscribed websites',
                          description=s,
                          color=discord.Colour.red())
    return embed


async def print_statement(s):
    embed = discord.Embed(title='Reminder',
                          description=s,
                          color=discord.Colour.red())
    for i in text_channel_list:
        await i.send(embed=embed)


async def channel_list():
    global db
    for guild in client.guilds:
        if not len(list(db.find({'id': guild.id}))):
            channel = await check(guild)
            db.insert_one({
                'id': guild.id,
                'websites': default_data,
                'remainder': 600,
                'channel': channel.id,
                'timezone': 'UTC',
                'server': guild.name
            })


async def roles():
    Remainder_data = list(db.find({}))
    for data in Remainder_data:
        guild = client.get_guild(data['id'])
        if discord.utils.get(guild.roles, name="Contest Reminder"):
            continue
        try:
            await guild.create_role(name="Contest Reminder", colour=discord.Colour(0xff0000))
        except:
            pass


async def reminder():
    global upcoming_data
    global db
    Remainder_data = list(db.find({}))
    for i in upcoming_data['objects']:
        if Time.check(i):
            for channel in Remainder_data:
                event = i['event']
                url = i['href']
                guild = client.get_guild(channel['id'])
                moderator = discord.utils.get(guild.roles, name="Contest Reminder")
                embed = discord.Embed(
                    title=' Reminder!!',
                    description=
                    f'Event: {event}\n Url: {url}\n Starts in 30 minutes',
                    color=discord.Colour.red())
                if channel['websites'].count(i['resource']):
                    channel = client.get_channel(channel['channel'])
                    try:
                        await channel.send(embed=embed)
                        if moderator:
                            await channel.send(f'{moderator.mention}')
                    except Exception as error:
                        channel = client.get_channel(895030489121980416)
                        await channel.send(error)
                        error_db = Data_base.error_data_base()
                        error_db.insert_one({'error': {str(traceback.format_exc())}})
                        pass


async def fetch():
    api = os.environ['api']
    while True:
        try:
            data = requests.get(
                f'https://clist.by:443/api/v2/contest/?start__gte={Time.time_url()}&order_by=start&{api}'
            )
        except Exception as error:
            error_db = Data_base.error_data_base()
            error_db.insert_one({'error': {str(traceback.format_exc())}})
            asyncio.sleep(60)
        global upcoming_data
        upcoming_data = data.json()
        await reminder()
        await asyncio.sleep(180)


@client.command()
async def subscribe(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Contest Remainder")
    user = ctx.message.author
    await user.add_roles(role)


@client.command()
async def unsubscribe(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Contest Remainder")
    user = ctx.message.author
    await user.remove_roles(role)


@client.event
async def on_ready():
    print("Bot is ready")
    await client.change_presence(activity=discord.Game(
        name="Responding to %help"))
    await roles()
    await channel_list()
    await fetch()


@client.command()
async def help(ctx):
    embed = main2.help_description()
    await ctx.send(embed=embed)


@client.command()
async def upcoming(ctx, arg):
    global supported_data
    global upcoming_data
    temp = db.find_one({'id': ctx.guild.id})
    if arg == 'subscribed' or arg == '':
        temp = list(filter(lambda x: temp['websites'].count(x['resource']) >= 1, upcoming_data['objects']))
    elif arg == 'all':
        temp = upcoming_data['objects']
    else:
        temp = list(
            filter(lambda x: x['resource'] == arg, upcoming_data['objects']))
        if len(temp) == 0:
            await ctx.send('No upcoming contests')
            return
    timezone = db.find_one({'id': ctx.guild.id})
    timezone = timezone['timezone']
    pages = main2.upcoming(temp, timezone)
    paginator = Paginator(pages=pages)
    await paginator.start(ctx)


@client.event
async def on_guild_join(guild):
    db.delete_one({'id': guild.id})
    channel = await check(guild)
    db.insert_one({
        'id': guild.id,
        'websites': default_data,
        'remainder': 600,
        'channel': channel.id,
        'timezone': 'UTC',
        'server': guild.name
    })
    embed = main2.help_description()
    await channel.send(embed=embed)
    await roles()


@client.command()
async def cur_website(ctx):
    temp = db.find_one({'id': ctx.guild.id})
    await ctx.send(embed=print_website(temp['websites']))


@client.command()
async def add_website(ctx, arg):
    try:
        if arg not in supported_data:
            await ctx.send("Incorrect website check %supported_website for all the supported websites")
            return
        db.update_one({'id': ctx.guild.id}, {'$push': {'websites': arg}})
        temp = db.find_one({'id': ctx.guild.id})
        await ctx.send(embed=print_website(temp['websites']))
    except Exception as error:
        await ctx.send("Some error occured")
        channel = client.get_channel(895030489121980416)
        await channel.send(error)


@client.command()
async def del_website(ctx, arg):
    try:
        if arg not in supported_data:
            return
        db.update_one({'id': ctx.guild.id}, {'$pull': {'websites': arg}})
        temp = db.find_one({'id': ctx.guild.id})
        await ctx.send(embed=print_website(temp['websites']))
    except Exception as error:
        await ctx.send("Some error occured")
        print(error)
        channel = client.get_channel(895030489121980416)
        await channel.send(error)


@client.command()
async def supported_website(ctx):
    s = 'Supported websites list - \n'
    for i in supported_data:
        s += f'{i}\n'
    embed = discord.Embed(title='Supported websites',
                          description=s,
                          color=discord.Colour.red())
    await ctx.send(embed=embed)


@client.command()
async def set_timezone(ctx, arg):
    if Time.check_timezone(arg):
        db.update_one({'id': ctx.guild.id}, {'$set': {'timezone': arg}})
        await ctx.send(f'Successfully updated time zone to {arg}')
    else:
        await ctx.send("Not a valid time zone")
        pages = Time.show_all_timezones()
        paginator = Paginator(pages=pages)
        await paginator.start(ctx)


@client.command()
async def change_channel(ctx):
    try:
        db.update_one({'id': ctx.guild.id}, {'$set': {'channel': ctx.channel.id}})
        await ctx.send('You will all reminders in this channel')
    except Exception as error:
        await ctx.send("Some error occured")
        channel = client.get_channel(895030489121980416)
        await channel.send(error)


token = os.environ.get('Token')
client.run(token)
