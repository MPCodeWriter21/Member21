#!usr/bin/python3
# Functions
# CodeWriter21

# Imports
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from telethon.errors.rpcerrorlist import PhoneCodeInvalidError, MessageIdInvalidError
from telethon.tl.functions.channels import JoinChannelRequest
from time import sleep
from .Constants import *
from datetime import datetime
import sys, os
code = ''
inp = input

# Prints text
def print(*args, end = '\n'):
	logger.print(*args, end = end)

# Gets input
def input(text):
	print (text, end='')
	return inp()

# Makes needed directories
def mkdirs():
	dirs = ['Backups', 'sessions', 'Subscribed channels', 'Logs']
	for dir in dirs:
		if (not os.path.exists(dir)) or (not os.path.isdir(dir)):
			os.mkdir(dir)
	logger.writel('Needed directories made')

# Exits
def Exit(text = ''):
	if not text:
		text = n + colors.Red + 'Exit' + end
	print (text)
	logger.writel('Exit')
	sys.exit()

# Clears console
def clear():
	os.system('clear || cls')
	logger.writel('Console cleared.')

# Extracts API information from config file
def get_api():
	logger.writel('Extracting API...')
	if not os.path.exists('config'):
		logger.writel('Config File Not Found!')
		raise Exception("Config File Not Found!")
	f = open('config', 'r')
	api_id = api_hash = ''
	for l in f.read().split('\n'):
		if l[:7] == 'api-id=':
			try:
				api_id = int(l[7:])
			except ValueError:
				pass
		elif l[:9] == 'api-hash=':
			api_hash = l[9:]
	if ((not api_id) and (api_id != 0)) or (not api_hash):
		logger.writel("Couldn't Extract API: Config File is Damaged!")
		raise Exception("Config File is Damaged")
	logger.writel('API Extracted.')
	return api_id, api_hash

# Saves new API information in config file
def set_api(api_id:int, api_hash:str):
	logger.writel('Setting API...')
	f = open('config', 'w')
	f.write(f"""# CodeWriter21
# Visit my.telegram.org

# Telegram API-id
api-id={api_id}

# Set Telegram API-hash
api-hash={api_hash}
""")
	logger.writel('API set.')
	f.close()

# Saves a backup of file
def Backup(path:str, name:str):
	fr = open(path, 'rb')
	data = fr.read()
	fr.close()
	fw = open(os.path.join('Backups', name), 'wb')
	fw.write(data)
	fw.close()
	logger.writel('Backup made: ' + name)

# Returns time as a string
def ttime():
	now = datetime.now()
	return f'{now.year}-{now.month}-{now.day} {now.hour}.{now.minute}.{now.second}'

# Tries to connect to Telegram
async def connect(client:TelegramClient):
	logger.writel('client is connecting...')
	try:
		print (a + colors.Yellow + "Connecting", end = '')
		for i in range(3):
			sleep(0.7)
			print (".", end = '')

		await client.connect()
		print (r + p + colors.Green + "Connected!!  \n" + end)
		logger.writel('client Connected.')
	except ConnectionError:
		logger.writel("Could't connect: ConnectionError!")
		print(r + n + colors.Red + "Couldn't connect!!" + end)
		print(n + colors.Pink + "Check your phone number(it must be like '+989999999999' or '+15555555555' or etc.)\n" + 
			n + colors.Pink + "Check your internet connection and if you are using VPN, Proxy or DNS try to fix it." + end)
		Exit()
	except KeyboardInterrupt:
		logger.writel("Connection Canceled: KeyboardInterrupt!")
		print(r + n + colors.Red + "Canceled!!" + end)
		Exit()
	except Exception as ex:
		logger.writel(f"Could't connect: {str(type(ex))} : {str(ex)}!")
		print(n + colors.Red + "Unknown Error:" + end, type(ex), ':', ex)
		Exit()

# Sends code request to telegram account and logins
async def login(client:TelegramClient, phone:str):
	global code
	logger.writel(f'client({phone}) is logging in...')
	def code_callback():
		global code
		if not code:
			code = input(a + colors.Blue + 'Enter Your Code : ' + colors.Cyan)
		return code
	while True:
		try:
			await client.start(phone=phone, code_callback=code_callback)
			logger.writel('client signed in.')
		except SessionPasswordNeededError:
			logger.writel('client needs 2step Password...')
			pwd = input(a + colors.Blue + 'Your 2step Password : ' + colors.Gray)
			await client.start(phone=phone, code_callback=code_callback, password=pwd)
			logger.writel('client signed in.')
			sleep(3)
		except PhoneCodeInvalidError:
			code = ''
			logger.writel('Invalid login code!')
			print (n + colors.Red + 'Invalid Login Code!!' + end)
		except KeyboardInterrupt:
			logger.writel('Login canceled: KeyboardInterrupt!')
			print (r + n + colors.Red + 'Login Canceled!' + end)
			Exit()
		except Exception as ex:
			logger.writel(f"Could't login: {str(type(ex))} : {str(ex)}!")
			print(n, type(ex), ':', ex)
			Exit()
		break

# Joins a channel or chat
async def join(client:TelegramClient, channel):
	logger.writel(f"Joining: {channel} ...")
	await client(JoinChannelRequest(channel))
	logger.writel(f"Joined: {channel} .")

# Adds channel to joined channels
def Add(ch_id:int, name):
	logger.writel(f"Saving subscribed channel: {ch_id} ...")
	f = open(os.path.join('Subscribed channels', 'SC' + str(name)), 'a')
	f.write(str(ch_id) + '\n')
	f.close()
	logger.writel(f"Subscribed channel saved: {ch_id} .")

# Leaves channel
async def leave(client:TelegramClient, me):
	logger.writel("Leaving subscribed channels...")
	f = open(os.path.join('Subscribed channels', 'SC' + str(me.id)), 'r')
	channels = f.read().split('\n')
	f.close()
	for channel in channels:
		try:
			await client.delete_dialog(int(channel))
			print (p + colors.Blue + 'Left: ' + channel + end)
			logger.writel(f"Left channel: {channel} .")
		except ValueError:
			logger.writel(f"Could't leave: {channel} .")
	logger.writel("Leaving end...")

# Joins a channel and clicks on a button to receive some points
async def Click(client:TelegramClient, msg, channel_username:str, row:int=1, column:int=0):
	logger.writel("Clicking...")
	try:
		me = await client.get_me()
		try:
			channel_url = msg.reply_markup.rows[1].buttons[1].url
		except AttributeError:
			return
		await join(client, channel_url)

		chan_entity = await client.get_entity(channel_url)

		try:
			result = await msg.click(row, column)
		except AttributeError:
			pass

		# Archives channel
		await client.edit_folder(entity=chan_entity, folder=1)
		logger.writel("Channel Archived...")

		Add(chan_entity.id, me.id)

		if not result:
			return

		try:
			print (p + colors.Green + f'Joined : {chan_entity.title} {colors.Red}->{colors.Green} {channel_username} : {result.message}')
			logger.writel(f'Joined : {chan_entity.title} -> {channel_username} : {result.message}')
		except UnicodeEncodeError:
			print (p + colors.Green + f'Joined : {chan_entity.id} {colors.Red}->{colors.Green} {channel_username}')
			logger.writel(f'Joined : {chan_entity.id} -> {channel_username}')
	except MessageIdInvalidError:
		logger.writel("Message Not Found!")
	except KeyboardInterrupt:
		logger.writel("Script Stoped by user: KeyboardInterrupt")
		print (r + n + colors.Red + 'Script Stoped by user!!')
		Exit()