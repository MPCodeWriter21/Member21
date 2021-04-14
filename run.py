#!/usr/bin/python3
# Main Script
# CodeWriter21

# Imports
try:
    from Files.Functions import *
    import socks, asyncio
    from telethon.errors import FloodWaitError
    from telethon import functions
    from Files.Exceptions import *
except KeyboardInterrupt:
    print('Script stopped by user!')
    exit()
except:
    print('Import failed!\nTry installing requirements : pip install -r requirements.txt\n' +
          'Try cloning Member21 again  : git clone https://GitHub.com/MPCodeWriter21/Member21')
    exit()

# Makes needed directories
mkdirs()

# Gets API information from config file
try:
    api_id, api_hash = get_api()
except APIConfigNotFoundException:
    print(r + n + colors.BackRed + 'APIConfig Not Found' + end + ' ' + co + colors.Red +
          " Couldn't find config file to get API!" + '\n' + a + colors.Yellow +
          'Please run configure.py to make APIConfig ' + co + colors.Blue + ' python3 configure.py' + end)
    Exit()
except APIConfigDamagedException:
    print(r + n + colors.BackRed + 'APIConfig Damaged' + end + ' ' + co + colors.Red +
          " Couldn't find API in config file!" + '\n' + a + colors.Yellow + 'Please run configure.py to set APIConfig '
          + co + colors.Blue + ' python3 configure.py' + end)
    Exit()

# Import
from Files.Config import *

logger.writel('Loading configs...')
# Loads BotConfigs data
configs = load_configs()
if len(configs) < 1:
    logger.writel('No BotConfig found!')
    raise NoBotConfigFoundException('No BotConfig Found!')
for config in configs:
    if config.enabled:
        if config.bot_id not in bots:
            bots.append(config.bot_id)
            bot_config_dict[config.bot_id] = config
        for ch in config.required_channels:
            if ch not in channels_to_join:
                channels_to_join.append(ch)
        if config.ads_channel not in ads_channels:
            ads_channels.append(config.ads_channel)
            channel_config_dict[config.ads_channel] = config
        if config.ads_channel not in channels_to_join:
            channels_to_join.append(config.ads_channel)
logger.writel('Configs loaded.')

if len(bots) < 1:
    logger.writel('No enabled BotConfig found!')
    raise NoBotEnabledConfigFoundException('No Enabled BotConfig Found!')

fwait = False
lmode = False

print(banner)
logger.writel('Banner printed.')
check_version()
logger.writel('Version Checked.')

logger.writel('Checking commandline inputs...')
# Checks the commandline inputs
import argparse

parser = argparse.ArgumentParser()
necessary_group = parser.add_argument_group('NECESSARY')
necessary_group.add_argument('--phone-number', '-n', metavar='[Phone Number]', action='store', type=str, dest='phone',
                             help='Your Phone Number')
optional_group = parser.add_argument_group('OPTIONAL')
optional_group.add_argument('--socks5-proxy', '-s', metavar='[SOCKS5 Proxy]', action='store', type=str, dest='psocks',
                            help='SOCKS5 Proxy to Connect to Telegram(Example: 127.0.0.1:9050)')
optional_group.add_argument('--http-proxy', '-H', metavar='[HTTP/HTTPS Proxy]', action='store', type=str, dest='phttp',
                            help='HTTP/HTTPS Proxy to Connect to Telegram(Example: 127.0.0.1:8000)')
optional_group.add_argument('--leave-mode', '-l', action='store_true', dest='lmode',
                            help='Use this option to leave saved channels in Subscribed channels directory')
args = parser.parse_args()
logger.writel('Commandline inputs checked.')

phone = args.phone
psocks = args.psocks
phttp = args.phttp

# Gets inputs from user
try:
    logger.writel('Getting inputs...')
    while not phone:
        phone = input(a + colors.Pink + f"Phone {co} " + colors.Cyan)
    if psocks == "tor":
        psocks = "127.0.0.1:9050"
    logger.writel('Got inputs.')
except KeyboardInterrupt:
    logger.writel("Canceled: KeyboardInterrupt!")
    print(r + n + colors.Red + "Cancelled!" + end)
    Exit()

logger.writel("Setting proxies...")
# Sets proxy settings
pr = None
if (not phttp) and psocks:
    host = psocks.split(':')[0]
    port = int(psocks.split(':')[1])
    pr = (socks.SOCKS5, host, port)
elif (not psocks) and phttp:
    host = phttp.split(':')[0]
    port = int(phttp.split(':')[1])
    pr = (socks.HTTP, host, port)

logger.writel("Making client...")
# Makes client variable
if pr:
    client = TelegramClient(os.path.join('sessions', 'session' + phone + '.session'), api_id, api_hash, proxy=pr)
else:
    client = TelegramClient(os.path.join('sessions', 'session' + phone + '.session'), api_id, api_hash)
logger.writel("Client made.")


# Handles flood wait error
def wait(s: int):
    global fwait
    for i in range(s):
        fwait = True
        sleep(1)
    fwait = False


# Main function of script
async def main():
    # Tries to connect to Telegram
    await connect(client)

    # Checks if user is logged in
    if not await client.is_user_authorized():
        logger.writel("Client is not authorized: Logging in...")
        # Logs in
        await login(client, phone)
        logger.writel("Client Logged in.")

        logger.writel("Making a backup of session...")
        # Backups session
        Backup(os.path.join('sessions', 'session' + phone + '.session'), 'Backup' + str(ttime()) + ' - session' + phone)
        logger.writel("Backup made.")

    # Clears console
    clear()
    print(banner)

    me = await client.get_me()
    logger.start(me)

    print(colors.Blue + 'Logged in as' + colors.BCyan, me.first_name, colors.Red + '(',
          end + colors.Cyan + phone, colors.Red + ')' + end)
    print()
    print(e)

    logger.writel("Joining required channels...")
    # Joins required channels
    for channel in channels_to_join:
        await join(client, channel)
    logger.writel("Joined.")

    logger.writel("Starting required bots...")
    # Starts required bots
    for bot in bots:
        await client.send_message(bot, "/start")
    logger.writel("Started.")

    times = {}

    for channel in ads_channels:
        posts = await client.get_messages(channel, 10)
        times[channel] = posts[0].date
        for msg in posts:
            try:
                await Click(client, msg, channel)
            except FloodWaitError:
                print(r + n + colors.Red + 'Flood Wait Error!!' + end)
                print(n + colors.Yellow + 'Waiting For Ten Minutes...' + end)
                wait(600)

    print(a + colors.Yellow + "Waiting for new channel to join..." + end + r, end='')

    # HACK:FIXME: There was a problem with the NewMessage event (could not receive all messages)
    #             so I wrote this loop to check for new messages every 10 seconds
    while True:
        for channel in ads_channels:
            new_posts = await client.get_messages(channel, 5)
            joined = None
            for post in new_posts:
                if post.date > times[channel]:
                    try:
                        await Click(client, post, channel)
                        joined = post.date
                    except FloodWaitError:
                        print(r + n + colors.Red + 'Flood Wait Error!!' + end)
                        print(n + colors.Yellow + 'Waiting For Ten Minutes...' + end)
                        wait(600)
                print(a + colors.Yellow + "Waiting for new channel to join..." + end + r, end='')
            if joined:
                times[channel] = joined
        sleep(21)


# Leaves all joined channels(saved in 'Subscribed channels' directory)
async def leave():
    logger.writel("Leaving Mode started...")
    # Tries to connect to Telegram
    await connect(client)

    # Checks if user is logged in
    if not await client.is_user_authorized():
        logger.writel("Client is not authorized: Logging in...")
        # Logs in
        await login(client, phone)
        logger.writel("Client Logged in.")

        logger.writel("Making a backup of session...")
        # Backups session
        Backup(os.path.join('sessions', 'session' + phone + '.session'), 'Backup' + str(ttime()) + ' - session' + phone)
        logger.writel("Backup made.")

    me = await client.get_me()
    logger.start(me)

    # Leaves
    await leave(client, me)


if __name__ == '__main__':
    try:
        if args.lmode:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(leave())
        else:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())

        client.run_until_disconnected()
    except ConnectionError:
        logger.writel("Script stopped because a connection error!")
        print(r + n + colors.Red + "Script stopped because a connection error!" + end)
        Exit()
    except KeyboardInterrupt:
        logger.writel("Script stopped by user: KeyboardInterrupt!")
        print(r + n + colors.Yellow + "Script stopped by user!" + end)
        Exit()
