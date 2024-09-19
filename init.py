from configparser import ConfigParser
from json import load

config = ConfigParser()
config.read('config.ini')
bot_cfg = config['bot']

token: str = bot_cfg['token']
lang: str = bot_cfg['language']
debug: bool = True if bot_cfg['debug'] == 'True' else False
send_timeout: int = int(bot_cfg['send_timeout'])
recv_timeout: int = int(bot_cfg['receive_timeout'])
users_file: str = bot_cfg['users_json']
addons: list = eval(bot_cfg['addons'])

admins_db: dict[int, int] = eval(bot_cfg['admins'])
with open(users_file, encoding='UTF-8') as json_file:
    json_db: dict[str, int] = load(json_file)
users_db: dict[int, int] = {int(key): value for key, value in json_db.items()}

commands: dict = dict()
triggers: dict = dict()

api_url: str = f'https://api.telegram.org/bot{token}/'

with open(f'lang/{lang}.json', encoding='UTF-8') as lang_file:
    inf_tpl: dict[str, str] = load(lang_file)

cur_offset: int = 0
