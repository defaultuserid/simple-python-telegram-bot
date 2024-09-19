from init import *
from importlib.util import module_from_spec, spec_from_file_location
from json import loads, dump
from re import match
from sys import modules
from time import strftime, sleep
from urllib.parse import quote
from urllib.request import urlopen


def show_info(info_txt: str, info_lvl: int, to_show: bool = debug) -> None:
    error_lvl: dict[int, str] = {
        0: 'OK',
        1: 'Received',
        2: 'Sent',
        3: 'Info',
        4: 'Warning',
        5: 'Error',
        6: 'Other',
    }

    cur_lvl: str = inf_tpl[error_lvl[info_lvl]]

    if to_show:
        print(f'{strftime("%Y-%m-%d - %H:%M:%S")} : {cur_lvl} {info_txt}')


def get_messages() -> list:
    upd_url: str = f'{api_url}getUpdates?offset={cur_offset}'
    rcv_data: dict = loads(urlopen(upd_url).read())
    msg_data: list = rcv_data.get('result', list())

    if rcv_data.get('ok'):
        if msg_data:
            show_info(inf_tpl['NewDataRcv'], 1)
        elif not msg_data:
            show_info(inf_tpl['NoNewData'], 1)
    else:
        show_info(inf_tpl['ErrRspFalse'].format(rcv_data), 5, True)
        raise RuntimeError

    return msg_data


def parse_message(inp_msg: dict) -> dict:
    upd_id: int = inp_msg['update_id']
    msg_type: str = 'message' if inp_msg.get('message') else 'edited_message'
    is_edit: bool = True if msg_type == 'edited_message' else False

    msg_form: dict = inp_msg[msg_type]
    from_id: int = msg_form['from']['id']
    is_bot: bool = msg_form['from']['is_bot']
    msg_txt: str = msg_form['text']

    show_info(inf_tpl['ParsedMsg'].format(upd_id, from_id, is_bot, is_edit, msg_txt), 3)

    return {
        'offset': upd_id,
        'user_id': from_id,
        'is_bot': is_bot,
        'is_edit': is_edit,
        'msg_txt': msg_txt,
    }


def find_action(msg_txt: str) -> tuple:
    msg_split: list = msg_txt.split(' ', 1)
    cmd_pref: str = msg_split[0]
    cmd_suf: str = msg_split[-1] if len(msg_split) > 1 else str()
    result: tuple = tuple()

    for command in commands:
        if cmd_pref.casefold() == command.casefold():
            show_info(inf_tpl['CmdFound'].format(command), 3)
            result = commands, command, commands[command][0], cmd_suf
            break

    if not result:
        for trigger in triggers:
            if match(trigger, msg_txt):
                show_info(inf_tpl['TrigFound'].format(trigger), 3)
                result = riggers, trigger, triggers[trigger][0]
                break

        show_info(inf_tpl['NoTrigOrCmd'].format(msg_txt), 3)

    return result


def has_access(user_id: int, act_lvl: int) -> bool:
    if user_id in admins_db:
        user_lvl: int = admins_db[user_id]
        show_info(inf_tpl['IDIsAdmin'].format(user_id, user_lvl), 3)
    elif user_id in users_db:
        user_lvl: int = users_db[user_id]

        if user_lvl >= 0:
            show_info(inf_tpl['IDIsUser'].format(user_id, user_lvl), 3)
        elif user_lvl < 0:
            show_info(inf_tpl['IDIsBanned'].format(user_id, user_lvl), 4)
    else:
        user_lvl: int = 0
        show_info(inf_tpl['IDIsUnknown'].format(user_id, user_lvl), 3)

    return True if user_lvl >= act_lvl else False


def do_action(act_data: tuple, msg_data: dict) -> None:
    act_tpl: str = 'IDUsesCmd' if act_data[0] == commands else 'IDUsesTrig'
    command: str = act_data[1]
    suffix: str = act_data[3]
    action: str | function = act_data[2]
    user_id: int = msg_data['user_id']

    if callable(action):
        show_info(inf_tpl[act_tpl].format(user_id, command), True)
        action(command=command, suffix=suffix, msg_data=msg_data, act_data=act_data)
    elif isinstance(action, str):
        show_info(inf_tpl[act_tpl].format(user_id, command), True)
        send_message(user_id, action)


def set_offset(new_offset: int) -> None:
    
    global cur_offset

    next_offset: int = new_offset + 1

    if new_offset >= cur_offset:
        cur_offset = next_offset
        show_info(inf_tpl['SetNewOff'].format(new_offset, next_offset), 3)
    elif new_offset < cur_offset:
        show_info(inf_tpl['RcvOldOff'].format(new_offset, cur_offset), 5, True)
        raise RuntimeError


def send_message(to_id: int, msg_txt: str) -> None:
    send_url: str = f'{api_url}sendMessage?chat_id={to_id}&text={quote(msg_txt)}'

    urlopen(send_url)
    show_info(inf_tpl['SentMsg'].format(to_id, msg_txt), 2, True)

    sleep(send_timeout)


def update_user_access(user_id: int, user_lvl: int) -> None:
    if user_id in admins_db:
        show_info(inf_tpl['DBNotForAdm'].format(user_id), 4, True)
    else:
        show_info(inf_tpl['DBSetIDLvl'].format(user_lvl, user_id), 3, True)
        users_db[user_id]: int = user_lvl

        show_info(inf_tpl['DBUpdInProg'], 3, True)
        with open(users_file, 'w', encoding='UTF-8') as users_json:
            dump(users_db, users_json)
        show_info(inf_tpl['DBUpdDone'], 3, True)


def addons_registrar():
    def registrar(module, groups: tuple):
        for (
            number,
            group,
        ) in enumerate(groups):
            group_type: dict = commands if number == 0 else triggers

            for command in group:
                action: str | None = group[command][0]
                acc_lvl: int = group[command][1]

                if isinstance(action, str):
                    group_type[command] = action, acc_lvl
                elif action is None:
                    group_type[command] = module.action, acc_lvl

    show_info(inf_tpl['RegAddons'], 3)

    for addon in addons:
        if addon.isidentifier():
            addon_name: str = f'addon_{addon}'
            addon_file: str = f'addons/{addon}.py'

            spec = spec_from_file_location(addon_name, addon_file)
            module_obj = module_from_spec(spec)
            modules[addon_name]: dict = module_obj
            spec.loader.exec_module(module_obj)

            registrar(module_obj, (module_obj.commands, module_obj.triggers))
        else:
            show_info(inf_tpl['RegWroName'].format(addon), 5, True)

    show_info(inf_tpl['RegAddDone'], 3)


def logic_loop():
    while True:
        for message in get_messages():
            pars_msg: dict = parse_message(message)
            user_id: int = pars_msg['user_id']
            msg_txt: str = pars_msg['msg_txt']
            is_bot: bool = pars_msg['is_bot']
            offset: int = pars_msg['offset']

            if (act_data := find_action(msg_txt)) and not is_bot:
                act_lvl: int = act_data[0][act_data[1]][1]

                if has_access(user_id, act_lvl):
                    do_action(act_data, pars_msg)

            set_offset(offset)

        sleep(recv_timeout)


def run_bot():
    try:
        show_info(inf_tpl['StartMsg'], 0, True)
        addons_registrar()
        logic_loop()
    except KeyboardInterrupt:
        show_info(inf_tpl['StopMsg'], 0, True)
