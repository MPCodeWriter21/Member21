#!usr/bin/python3
# Main Script
# CodeWriter21

# Imports
try:
	from Files.Functions import *
	import socks, asyncio
	from telethon.errors import FloodWaitError
except KeyboardInterrupt:
	print ('Script stopped by user!')
	Exit()
except:
	print ('Import failed!\nTry installing requirements : pip install requirements.txt\nTry cloning Member21 again  : git clone https://GitHub.com/MPCodeWriter21/Member21')
	exit()

# Makes needed directories
mkdirs()

# Gets API information from config file
api_id, api_hash = get_api()

fwait = False
lmode = False

print (banner)
logger.writel('Banner printed.')

logger.writel('Checking commandline inputs...')
# Checks the commandline inputs
import argparse
parser = argparse.ArgumentParser()
necessary_group = parser.add_argument_group('NECESSARY')
necessary_group.add_argument('--phone-number', '-n', metavar='[Phone Number]', action='store', type=str, dest='phone', help='Your Phone Number')
optional_group = parser.add_argument_group('OPTIONAL')
optional_group.add_argument('--socks5-proxy', '-s', metavar='[SOCKS5 Proxy]', action='store', type=str, dest='psocks', help='SOCKS5 Proxy to Connect to Telegram(Example: 127.0.0.1:9050)')
optional_group.add_argument('--http-proxy', '-H', metavar='[HTTP/HTTPS Proxy]', action='store', type=str, dest='phttp', help='HTTP/HTTPS Proxy to Connect to Telegram(Example: 127.0.0.1:8000)')
optional_group.add_argument('--leave-mode', '-l', action='store_true', dest='lmode', help='Use this option to leave saved channels in Subscribed channels directory')
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
	client = TelegramClient(os.path.join('sessions', 'session'+phone+'.session'), api_id, api_hash,proxy=pr)
else:
	client = TelegramClient(os.path.join('sessions', 'session'+phone+'.session'), api_id, api_hash)
logger.writel("Client made.")


# Handles flood wait error
def wait(s:int):
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
		Backup(os.path.join('sessions', 'session'+phone+'.session'), 'Backup' + str(ttime()) + ' - session'+phone)
		logger.writel("Backup made.")

	#Clears console
	clear()
	print (banner)

	me = await client.get_me()
	logger.start(me)


	logger.writel("Joining required channels...")
	# Joins required channels
	for channel in channels:
		await join(client, channel)
	logger.writel("Joind.")

	logger.writel("Starting required bots...")
	# Starts required bots
	for bot in bots:
		await client.send_message(bot, "/start")
	logger.writel("Started.")


	posts = await client.get_messages(Speed_channel, 21)
	for msg in posts:
		try:
			await Click(client, msg, Speed_channel)
		except FloodWaitError:
			print(n + colors.Red + 'Flood Wait Error!!' + end)
			print(n + colors.Yellow + 'Waiting For Five Minutes...' + end)
			wait(300)
	posts = await client.get_messages(Tel_channel, 21)
	for msg in posts:
		try:
			await Click(client, msg, Tel_channel)
		except FloodWaitError:
			print(n + colors.Red + 'Flood Wait Error!!' + end)
			print(n + colors.Yellow + 'Waiting For Five Minutes...' + end)
			wait(300)


	print (a + colors.Yellow + "Waiting for new channel to join..." + end + r, end = '')	

# Leaves all joined channels(saved in 'Subscribed channels' directory)
async def Leave():
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
		Backup(os.path.join('sessions', 'session'+phone+'.session'), 'Backup' + str(ttime()) + ' - session'+phone)
		logger.writel("Backup made.")

	me = await client.get_me()
	logger.start(me)

	# Leaves
	await leave(client, me)

# NewMessage Event handler
@client.on(events.NewMessage())
async def handler(event):
	if fwait or lmode:
		return

	if event.message.to_id.channel_id in [1449235459, 1245473872]:
		chans = {1449235459 : Speed_channel, 1245473872 : Tel_channel}
		try:
			await event.mark_read()
			await Click(client, event.message, chans[event.message.to_id.channel_id])
			print (a + colors.Yellow + "Waiting for new channel to join..." + end + r, end = '')		
		except FloodWaitError:
			print(n + colors.Red + 'Flood Wait Error!!' + end)
			print(n + colors.Yellow + 'Waiting For Five Minutes...' + end)
			wait(300)
		except:
			print(n + colors.Red + 'Error!!' + end)
		try:
			sleep(2)
		except KeyboardInterrupt:
			print (r + n + colors.Yellow + "Script Stoped by user!!" + end)
			Exit()

if __name__ == '__main__':
	try:
		if args.lmode:
			loop = asyncio.get_event_loop()
			loop.run_until_complete(Leave())
		else:
			loop = asyncio.get_event_loop()
			loop.run_until_complete(main())
		
		client.run_until_disconnected()
	except ConnectionError:
		logger.writel("Script stopped because a connection error!")
		print(n + colors.Red + "Script stopped because a connection error!" + end)
		Exit()
	except KeyboardInterrupt:
		logger.writel("Script stopped by user: KeyboardInterrupt!")
		print(r + n + colors.Yellow + "Script stopped by user!" + end)
		Exit()