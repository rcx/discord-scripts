import requests
from collections import defaultdict
import time
import random
import json

baseurl = "https://discordapp.com/api/v6"
auth_token = ''
search_query = '/guilds/xxx/messages/search?author_id=xxx&include_nsfw=true&sort_by=timestamp&sort_order=asc&offset=0'
delay = 1.0

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

def search_messages(query):
    result = api_request(query)
    return [message for group in result['messages'] for message in group if 'hit' in message]

def delete_message(channel_id, message_id):
    api_request('/channels/' + channel_id + '/messages/' + message_id, method='DELETE')

while True:
    messages = search_messages(search_query)
    if not messages:
        break
    for m in messages:
        print(m['id'], m['author']['username'] + '#' + m['author']['discriminator'], ':', m['content'])
        delete_message(m['channel_id'], m['id'])
