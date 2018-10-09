import discord
import json

class CommandHandler:

    def __init__(self, client):
        self.client = client
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def command_handler(self, message):
        for command in self.commands:
            if message.content.startswith(command['trigger']):
                args = message.content.split(' ')
                if args[0] == command['trigger']:
                    args.pop(0)
                    if command['args_num'] == 0:
                        return self.client.send_message(message.channel, str(command['function'](message, self.client, args)))
                        break
                    else:
                        if len(args) >= command['args_num']:
                            return self.client.send_message(message.channel, str(command['function'](message, self.client, args)))
                            break
                        else:
                            return self.client.send_message(message.channel, 'command "{}" requires {} argument(s) "{}"'.format(command['trigger'], command['args_num'], ', '.join(command['args_name'])))
                            break
                else:
                    break



client = discord.Client()
token = 'NDk5MjE3NjY3MjkxNjExMTM2.Dp5FbQ.3RKfqyXujzfXuXwXA6u88j8h9NQ'

ch = CommandHandler(client)


def commands_command(message, client, args):
    try:
        count = 1
        coms = '**Commands List**\n'
        for command in ch.commands:
            coms += '{}.) {} : {}\n'.format(count, command['trigger'], command['description'])
            count += 1
        return coms
    except Exception as e:
        print(e)
ch.add_command({
    'trigger': '!commands',
    'function': commands_command,
    'args_num': 0,
    'args_name': [],
    'description': 'Prints a list of all the commands!'
})

def ip_command(message, client, args):
    try:
        req = requests.get('http://ip-api.com/json/{}'.format(args[0]))
        resp = json.loads(req.content.decode())
        if req.status_code == 200:
            if resp['status'] == 'success':
                template = '**{}**\n**IP: **{}\n**City: **{}\n**State: **{}\n**Country: **{}\n**Latitude: **{}\n**Longitude: **{}\n**ISP: **{}'
                out = template.format(args[0], resp['query'], resp['city'], resp['regionName'], resp['country'], resp['lat'], resp['lon'], resp['isp'])
                return out
            elif resp['status'] == 'fail':
                return 'API Request Failed'
        else:
            return 'HTTP Request Failed: Error {}'.format(req.status_code)
    except Exception as e:
        print(e)
ch.add_command({
    'trigger': '!ip',
    'function': ip_command,
    'args_num': 1,
    'args_name': ['IP\Domain'],
    'description': 'Prints information about provided IP/Domain!'
})

@client.event
async def on_ready():
    try:
        print(client.user.name)
        print(client.user.id)
    except Exception as e:
        print(e)


@client.event
async def on_message(message):
    
    if message.author == client.user:
        pass
    else:
       
        try:
            await ch.command_handler(message)
   
        except TypeError as e:
            pass
       
        except Exception as e:
            print(e)

      
            
client.run(token)
