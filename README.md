# ASMagic

## Short introduction

This bot has been created with ❤️ by [@jan123](https://telegram.me/jan123) to help people administrate their groups, and includes many useful tools.

MagicAntiSpam bot was born as a python [telebot](https://github.com/eternnoir/pyTelegramBotAPI) it has been turned into an administration bot.

#### MagicAntiSpam on Telegram:

- [`@ASMagicBot`](https://telegram.me/ASMagicBot)
    - **_branch_**: `master`
    - **_channel_**: [`@MagicNews`](https://telegram.me/MagicNews).
    - **_group_**: [`Support Group`](https://telegram.me/joinchat/AAAAAECPv8joesRabLdkGg).

* * *

## Setup
List of required packages:
- `python2.7`
- `redis-server`

You will need some other Python modules too, which can be (and should be) installed through the Python package manager(pip)

**Installation**

You can easily install MagicAntiSpam by running the following commands:

```bash
# Tested on Ubuntu 16.04

$ wget https://raw.githubusercontent.com/MagicNews/ASMagic/master/install.sh
$ bash install.sh
```
or

```bash
# Tested on Ubuntu 14.04, 15.04 and 16.04, Debian 7, Linux Mint 17.2

$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install python2.7 python-pip

# We are going now to install the required Python modules

$ pip install --upgrade requests
$ pip install --upgrade redis
$ pip install --upgrade pytelegrambotapi

# Clone the repository and give the launch script permissions to be executed

$ git clone https://github.com/MagicNews/ASMagic.git
$ cd ASMagic
$ sudo chmod 777 launch.sh
$ mv ./usr/local/lib/python2.7/dist-packages/telebot /
```
Other things to check before running the bot:

**First of all, take a look at your bot settings:**

> • Make sure privacy is disabled (more info can be found by heading to the [official Bots FAQ page](https://core.telegram.org/bots/faq#what-messages-will-my-bot-get)). Send `/setprivacy` to [@BotFather](http://telegram.me/BotFather) to check the current status of this setting.

**Before you do anything else, open config.py (in a text editor or nano) and make the following changes:**

> • Set `token` to the authentication token that you received from [`@BotFather`](http://telegram.me/BotFather).
>
> • Insert your numerical Telegram ID into the `sudos` table. Other superadmins can be added too. It is important that you insert the numerical ID and NOT a string.
>
> • Insert your admins numerical Telegram ID into the `admins` table. Other superadmins can be added too. It is important that you insert the numerical ID and NOT a string.
>
> • Set your `log_chat` (the ID of the chat where the bot will send all the bad requests received from Telegram) and your `errors_chat` (the ID of the chat that will receive execution errors).


Before you start the bot, you have to start the Redis process.
```bash
# Start Redis

$ sudo service redis-server start
```

## Starting the process

To start the bot, run `./launch.sh`. To stop the bot, press Control <kbd>CTRL</kbd>+<kbd>C</kbd> twice.

You may also start the bot with `python bot.py`, however it will not restart automatically.

* * *

## Some notes about the database

*Everything* is stored on Redis, and the fastest way to edit your database is via the [Redis CLI](http://redis.io/topics/rediscli).

You can find a backup of your Redis database in `/etc/redis/dump.rdb`. The name of this file and the frequency of saves are dependent on your redis configuration file.

* * *

## Credits

[eternnoir](https://github.com/eternnoir), for [telebot](https://github.com/eternnoir/pyTelegramBotAPI)

All the people who reported bugs and suggested new stuffs

Good Luck:)
