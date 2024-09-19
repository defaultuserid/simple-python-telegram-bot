from functions import send_message

commands = {'/ping': (None, 1)}
triggers = {}


def action(**args: dict) -> None:
    user_id: int = args['msg_data']['user_id']
    send_message(user_id, 'pong!')
