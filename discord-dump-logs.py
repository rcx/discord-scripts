import requests
from collections import defaultdict
import time
import random
import json

baseurl = "https://discordapp.com/api/v6"
auth_token = ''
chan_id = ''

def api_request(path):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.306 Chrome/78.0.3904.130 Electron/7.1.11 Safari/537.36",
        'Authorization': auth_token
    }

    delay = 1.0 + 1.0 * random.random()
    time.sleep(delay)
    return requests.get(baseurl + path, headers=headers).json()

def channel_messages(channel_id):
    members = api_request('/channels/' + channel_id + '/messages?limit=100')
    while members:
        for m in members: # or yield from in python3.3
            yield m
        cursor = members[-1]['id']
        print cursor
        members = api_request('/channels/' + channel_id + '/messages?limit=100&before=' + cursor)

f = open('discord_dump.txt', 'a')
for m in channel_messages(chan_id):
    json.dump(m, f)
    f.write('\n')
print 'Done'
