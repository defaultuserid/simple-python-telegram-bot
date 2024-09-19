# Simple-Python-Telegram-Bot

A simple python telegram bot that uses the official [bot-api](https://core.telegram.org/bots/api) for its magic.\
Builtin modules were used: `configparser, re, time, json, urllib`.\
Mostly proof of concept.

## Features

1. Multilingual support (currently supports: **en**, **ru**)
2. Simple configuration file: `bot.ini`
3. User access levels: `3 admin, 2 trusted, 1 registered, 0 unregistered, -1 banned`
4. Modules support for triggers\commands or etc.
5. Informative mode, just set `debug = True` in `bot.ini`

## How to install and run bot

1. Clone repo.
2. Edit `bot.ini` to set [bot token](https://core.telegram.org/bots/features#botfather) and admins.
3. Run `python main.py`
4. Done!

## Configuration file

    [bot]
    token = 0123456789:AAAAAAAAAA-BBBBBBBBBBBBBBBBBBBBBBBB
    language = en
    debug = False
    send_timeout = 1
    receive_timeout = 4
    admins = {0000000000: 3, 0123456789: 3}

Get bot token [here](https://core.telegram.org/bots/features#botfather) and replace default
token `0123456789:AAAAAAAAAA-BBBBBBBBBBBBBBBBBBBBBBBB` with it.\
`language` set to **en** or **ru**.\
`debug` set to `True` to see in detail what is going on.\
`send_timeout` amount of time in seconds for delay between sending each message.\
`receive_timeout` amount of time in seconds for delay between receiving messages from telegram.\
`admins` has scheme: `{AdminID1: AccessLevel, AdminID2: AccessLevel, AdminID3: AccessLevel}`

_**To stop bot press:**_ `Ctrl+C`

**Enjoy!**
