import requests
from collections import defaultdict
import time
import random
import json
import os

baseurl = "https://discordapp.com/api/v6"
auth_token = ''
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
        members = api_request('/channels/' + channel_id + '/messages?limit=100&before=' + cursor)

def delete_message(channel_id, message_id):
    api_request('/channels/' + channel_id + '/messages/' + message_id, method='DELETE')

author_id = api_request('/users/@me')['id']
print('My id is ' + author_id)
if not os.path.exists('logs'):
    os.mkdir('logs')
elif not os.path.isdir('logs'):
    print('logs/ already exists, please delete it')
    exit(1)
for channel in api_request('/users/@me/channels'):
    chan_id = channel['id']
    name = ''
    if 'name' in channel:
        name = channel['name']
    if not name:
        name = ','.join(map(lambda recipient: recipient['username'], channel['recipients']))
    filename = os.path.join('logs', name) + '.txt'
    print(filename)
    with open(filename, 'a') as f:
        for m in channel_messages(chan_id):
            message_id = m['id']
            if m['author']['id'] == author_id:
                delete_message(chan_id, message_id)
            f.write(str(m) + '\n')
            print(message_id, m['author']['username'] + '#' + m['author']['discriminator'], ':', m['content'])
# print 'Done'
