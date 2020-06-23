import requests
from collections import defaultdict
import time

baseurl = "https://discordapp.com/api/v6"
auth_token = ''
delay = 0.250

def api_request(path):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.306 Chrome/78.0.3904.130 Electron/7.1.11 Safari/537.36",
        'Authorization': auth_token
    }

    time.sleep(delay)
    return requests.get(baseurl + path, headers=headers).json()

def guild_members(guild_id):
    members = api_request('/guilds/' + guild_id + '/members?limit=1000')
    while members:
        for m in members: # or yield from in python3.3
            yield m
        cursor = members[-1]['user']['id']
        members = api_request('/guilds/' + guild_id + '/members?limit=1000&after=' + cursor)

guild_names = {}
user_names = {}
guild_table = defaultdict(set)

def process_guild(guild_id):
    for member in guild_members(guild_id):
        user = member['user']
        member_id, member_name = user['id'], user['username'] + '#' + user['discriminator']
        user_names[member_id] = member_name
        guild_table[guild_id].add(member_id)
        print(member_id, member_name)

if __name__ == '__main__':
    process_guild('guild_id_here')

