import toml

config = toml.load('settings.toml')
api_id = config['telegram']['api_id']
api_hash = config['telegram']['api_hash']
bot_token = config['telegram']['bot_token']
channel_id = config['telegram']['channel_id']
token = config['vk']['token']
group_id = config['vk']['group_id']