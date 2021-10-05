import datetime
from time import strftime, gmtime
import discord
import pytz


def time_url():
    time = strftime('%Y-%m-%d %H:%M:%S', gmtime())
    time = time.replace(' ', 'T')
    time = time.replace(':', '%3A')
    return time


def check(i):
    time = strftime('%Y:%m:%d %H:%M:%S', gmtime())
    start_time = i['start']
    start_time = start_time.replace('-', ':')
    start_time = start_time.replace('T', ' ')
    FMT = '%Y:%m:%d %H:%M:%S'
    tdelta = datetime.datetime.strptime(start_time, FMT) - datetime.datetime.strptime(time, FMT)
    if 1800 <= tdelta.total_seconds() <= 1980:
        return 1
    else:
        return 0


def check_timezone(timezone):
    for tz in pytz.all_timezones:
        if tz == timezone:
            return 1
    return 0


def show_all_timezones():
    pages = []
    j = 0
    description = ""
    for tz in pytz.all_timezones:
        j = j + 1
        description += f'{tz}\n'
        if j % 15 == 0:
            description += f'All vaild time zones are avaliable here https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568 \n Page no. {j / 15}'
            embed = discord.Embed(
                title="Valid time zones",
                description=description,
                color=discord.Colour.red()
            )
            pages.append(embed)
            description = ""
    if j % 15 != 0:
        description += f'Page no. {j / 15}'
        embed = discord.Embed(
            title="Valid time zones",
            description=description,
            color=discord.Colour.red()
        )
        pages.append(embed)
    return pages

