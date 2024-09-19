from init import users_db
from functions import send_message, update_user_access

commands = {'/start': (None, 0), '/stop': (None, 1)}
triggers = {}


def action(**args: dict) -> None:
    command: str | function = args['command']
    user_id: int = args['msg_data']['user_id']

    if command == '/start':
        update_user_access(user_id, 1)
        send_message(user_id, 'Hello!')
    elif command == '/stop':
        update_user_access(user_id, 0)
        send_message(user_id, 'Bye-Bye!')
