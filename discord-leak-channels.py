import requests
from collections import defaultdict
import time
import json

baseurl = "https://discordapp.com/api/v6"
auth_token = fillmein
guild_id = fillmein
delay = 0.250

def api_request(path):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.306 Chrome/78.0.3904.130 Electron/7.1.11 Safari/537.36",
        'Authorization': auth_token
    }

    time.sleep(delay)
    return requests.get(baseurl + path, headers=headers).json()

chans = api_request('/guilds/' + guild_id + '/channels')
print json.dumps(chans, indent=2)

roles = api_request('/guilds/' + guild_id + '/roles')
print json.dumps(roles, indent=2)