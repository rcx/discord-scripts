#!/usr/bin/env python3
import requests
from collections import defaultdict
import time
import random
import json
import os
import csv

baseurl = "https://discordapp.com/api/v9"
auth_token = 'mfa.your.token.goes.here'
delay = 1.5

def api_request(path, method='GET'):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.309 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
        'Authorization': auth_token
    }

    time.sleep(delay + max(0, random.gauss(1.0,0.5))) # adjust speed to preference
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
    return api_request('/channels/' + channel_id + '/messages/' + message_id, method='DELETE')

if not os.path.exists('deleted.txt'):
    open('deleted.txt', 'w+').close()
cache = open('deleted.txt', 'r+')
already_deleted = set(cache.read().splitlines())
cache.seek(0, os.SEEK_END) # ??? avoid IOerror when using a r+ for write after reading
with open('messages/index.json', 'r', encoding='utf-8') as index:
    index = json.load(index)
for channel_id in index:
    with open('messages/' + channel_id + '/channel.json', 'r', encoding='utf-8') as channel:
        channel = json.load(channel)
    name = ''
    if 'guild' in channel:
        guild = channel['guild']
        if 'name' in guild:
            name += guild['name']
        else:
            name += guild['id']
        name += '#'
    if 'name' in channel and channel['name'] is not None:
        name += channel['name']
    else:        
        name += channel['id']
    print(channel_id + ': ' + name)
    if channel_id in already_deleted: # based snowflakes unique across all types
        print('* This whole channel is done already')
        continue
    num_404s = 0
    with open('messages/' + channel_id + '/messages.csv', 'r', encoding='utf-8') as messages:
        messages = csv.reader(messages, delimiter=",", quotechar='"')
        next(messages, None) # skip header
        for message in messages:
            message_id,timestamp,contents,attachments = message
            print(timestamp,contents,attachments)
            if message_id in already_deleted:
                print('* Already deleted')
                continue
            resp = delete_message(channel_id, message_id)
            if resp.status_code >= 300:
                print('! Got ' + str(resp.status_code))
            if resp.status_code == 404:
                num_404s += 1
                if num_404s > 5:
                    print("* Received 5 404s, we skip this channel")
                    break
            if (200 <= resp.status_code) < 300 or (resp.status_code == 404):
                cache.write(message_id + '\n')
    cache.write(channel_id + '\n')
