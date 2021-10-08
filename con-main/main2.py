import datetime
import math
from time import strftime, gmtime

import discord


def seconds_to_days(seconds):
    converted = ''
    converted += f'{math.floor(seconds / (3600 * 24))} days '
    seconds = seconds % (3600 * 24)
    converted += f'{math.floor(seconds / 3600)} hours '
    seconds = seconds % (3600)
    converted += f'{math.floor(seconds / 60)} minutes '
    return converted


def upcoming(data, zone):
    pages = []
    j = 0
    description = ""
    for i in data:
        # start_time = i['start']
        # start_time = start_time.replace('T', ' ')
        # FMT = '%Y-%m-%d %H:%M:%S'
        # time = datetime.datetime.strptime(start_time, FMT)
        # t = time.replace(tzinfo=datetime.timezone.utc).astimezone(timezone(zone))
        event = i['event']
        resource = i['resource']
        url = i['href']
        time = strftime('%Y:%m:%d %H:%M:%S', gmtime())
        start_time = i['start']
        start_time = start_time.replace('-', ':')
        start_time = start_time.replace('T', ' ')
        FMT = '%Y:%m:%d %H:%M:%S'
        tdelta = datetime.datetime.strptime(start_time, FMT) - datetime.datetime.strptime(time, FMT)
        converted_to_days = seconds_to_days(tdelta.total_seconds())
        resource = resource[0:len(resource) - 4].upper()
        description += f'[{resource}]({url}): \n{event}\n Starts in {converted_to_days} \n \n'
        j = j + 1
        if j % 6 == 0:
            embed = discord.Embed()
            embed.title = "UPCOMING CONTEST"
            embed.description = description
            embed.set_footer(text=f'Page no. {j / 6}')
            embed.color = discord.Colour.blue()
            pages.append(embed)
            description = ""
    if j % 6 != 0:
        embed = discord.Embed()
        embed.title = "UPCOMING CONTEST"
        embed.description = description
        embed.color = discord.Colour.blue()
        embed.set_footer(text=f'Page no. {math.ceil(j / 6)}')
        pages.append(embed)
    return pages


def help_description():
    embed = discord.Embed()
    embed.title = 'Contest reminder'
    embed.add_field(name='Description', inline=False, value='This bot reminds you 30 minutes before the contest from '
                                                            'all your subscribed websites')
    embed.add_field(name="Prefix - %", value="Example- %help", inline=False)
    embed.color = discord.Colour.green()
    description = '1) **%upcoming all** \n shows all the upcoming contests of all the websites \n' \
                  '2) **%upcoming subscribed** \n shows all the upcoming contests of all the subscribed websites \n' \
                  '3) **%upcoming <url of the website>** \n' \
                  'Example - %upcoming codeforces.com shows all the upcoming contests of codeforces \n' \
                  '4) **%cur_website** shows all your subscribed websites \n' \
                  'There are some default websites already subscribed for you check them out \n' \
                  '5) **%add_website <url of website>** - subscribes to this website \n' \
                  'Example - %add_website codeforces.com \n adds codeforces to your subscribed websites\n' \
                  '6) **%del_website <url of website>** - Deletes subscription of this website \n' \
                  'Example - %del_website codeforces.com \n deletes codeforces from your subscribed websites \n' \
                  '7) **%supported_website** - Shows all the supported websites \n' \
                  '8) **%change_channel** - Recieve further updates in that channel \n' \
                  '9) **%subscribe** - Adds Contest Remainder role to recive remainders mentions\n' \
                  '10) **%unsubscribe** - Removes Contest Remainder role \n'
    embed.add_field(name="List of commands", value=description, inline=False)
    embed.add_field(name="Note",
                    value='Like the project star the [repo](https://github.com/Ksathwik03/contest_remainder) ✌',
                    inline=False)
    embed.add_field(name="Contribute", value="[github link](https://github.com/Ksathwik03/contest_remainder)",
                    inline=True)
    embed.add_field(name="Invite link", value="[Bot link](https://discord.com/oauth2/authorize?client_id"
                                              "=860779669288779776&permissions=8&scope=bot)",
                    inline=True)

    return embed


time_store = {'s': 1, 'm': 60, 'h': 3600, 'd': 3600 * 24}


def validate(time):
    if len(time) < 2:
        return -1
    time_num = time[0:len(time) - 1]
    time_str = time[len(time) - 1]
    check = list(filter(lambda i: i == time_str, time_store))
    if len(check) and time_num.isnumeric():
        return int(time_num) * time_store[check[0]]
    print(check)
    return -1
