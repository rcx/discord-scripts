import requests
from collections import defaultdict
import time
import random
import json

baseurl = "https://discordapp.com/api/v6"
auth_token = ''
chan_id = ''
author_id = ''
delay = 1.5

def api_request(path, method='GET'):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.306 Chrome/78.0.3904.130 Electron/7.1.11 Safari/537.36",
        'Authorization': auth_token
    }

    time.sleep(delay + max(0, random.gauss(1.0,0.5)))
    if method == 'GET':
        return requests.get(baseurl + path, headers=headers).json()
    elif method == 'DELETE':
        return requests.delete(baseurl + path, headers=headers)
    else:
        raise ValueError("unsupported method")

def channel_messages(channel_id):
    members = api_request('/channels/' + channel_id + '/messages?limit=100')
    while members:
        for m in members: # or yield from in python3.3
            yield m
        cursor = members[-1]['id']
        print cursor
        members = api_request('/channels/' + channel_id + '/messages?limit=100&before=' + cursor)

def delete_message(channel_id, message_id):
    api_request('/channels/' + channel_id + '/messages/' + message_id, method='DELETE')

for m in channel_messages(chan_id):
    message_id = m['id']
    print(message_id, m['author']['username'] + '#' + m['author']['discriminator'], ':', m['content'])
    if m['author']['id'] == author_id:
        print('Deleting this message.')
        delete_message(chan_id, message_id)
print 'Done'
