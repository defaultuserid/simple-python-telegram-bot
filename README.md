# Simple-Python-Telegram-Bot

A simple python telegram bot that uses the official [bot-api](https://core.telegram.org/bots/api) for its magic.\
Uses modules from python's built-in library.

## Features

1. Multilingual support (currently only supports **en**)
2. Simple configuration file: `config.ini`
3. User access levels: `3 admin, 2 trusted, 1 registered, 0 unregistered, -1 banned`
4. Support modules for triggers/commands.
5. Informative and easy-to-use.

## How to install and run bot

1. Clone repo.
2. Edit `config.ini` to set [bot token](https://core.telegram.org/bots/features#botfather) and admins.
3. Run `python main.py`
4. Done!

## Configuration file

    [bot]
    token = 0123456789:AAAAAAAAAA-AAAAAAAAAAAAAAAAAAAAAAAA
    language = en
    debug = False
    send_timeout = 2
    receive_timeout = 4
    admins = {1111111111: 3, 1234567890: 3}
    users_json = users.json
    addons = ['start', 'stop', 'help', 'cats']

* **token** — get bot token [here](https://core.telegram.org/bots/features#botfather) and replace default token with it.
* **language** — language used for information messages, `en` or `ru`.
* **debug** — set to `True` to see in detail what is going on.
* **send_timeout** — amount of time in seconds for delay between sending each message.
* **receive_timeout** — amount of time in seconds for delay between receiving messages from telegram.
* **admins** — has scheme `{AdminID1: AccessLevel, AdminID2: AccessLevel, AdminID3: AccessLevel}`
* **users_json** — file where user IDs will be saved in **json** format.
* **addons**  — addons that the bot will automatically load at startup: `['addon1', 'addon2', 'addon3']`

_**To stop bot press:**_ `Ctrl+C`

**Enjoy!**
