# Python3
# Constants
# CodeWriter21

# Imports
import platform
from .Loging import log

# System
windows = (platform.system() == 'Windows')

# Colors
class colors:
	Gray   = '\033[90m'
	Red    = '\033[91m'
	Green  = '\033[92m'
	Yellow = '\033[93m'
	Blue   = '\033[94m'
	Pink   = '\033[95m'
	Cyan   = '\033[96m'
	BCyan  = '\033[1;96m'
	White  = '\033[1;37m'

# Clears colors if system is windows
if windows:
	colors.Gray   = ''
	colors.Red    = ''
	colors.Green  = ''
	colors.Yellow = ''
	colors.Blue   = ''
	colors.Pink   = ''
	colors.Cyan   = ''
	colors.BCyan  = ''
	colors.White  = ''

# Useful things
end = '' if windows else '\033[0m'
r   = '\r'
e   = colors.White + '===================================================' + end
a   = f'{colors.Cyan}[' + ('' if windows else '\033[35m') + f'={colors.Cyan}] ' + end
p   = f'{colors.Yellow}[{colors.Green}+{colors.Yellow}] ' + end
n   = f'{colors.Yellow}[{colors.Red}-{colors.Yellow}] ' + end
co  = colors.Red + ':' + end

# Banner
banner = colors.Cyan + r"""
 __  __                _              ____  _
|  \/  | ___ _ __ ___ | |__   ___ _ _|___ \/ |
| |\/| |/ _ \ '_ ` _ \| '_ \ / _ \ '__|__) | |
| |  | |  __/ | | | | | |_) |  __/ |  / __/| |
|_|  |_|\___|_| |_| |_|_.__/ \___|_| |_____|_|
""" + f"""{e}
{colors.White}Blog      {co} {colors.Cyan} https://www.{colors.BCyan}CodeWriter21{end + colors.Cyan}.blogsky.com
{colors.White}Github    {co} {colors.Cyan} http://www.GitHub.com/{colors.BCyan}MPCodeWriter21
{colors.White}Telegram  {co} {colors.Cyan} https://www.Telegram.me/{colors.BCyan}CodeWriter21
{e}
"""

# Usernames
Speed_channel = '@orderspeedmember'
Tel_channel = '@TelMemberbots'
channels = ['orderspeedmember', 'TelMemberbots', 'TelMembere', 'TelHediye', 'PEAGES']
bots = ['member_speedrobot', 'TelMembers_Bot']

# Logger
logger = log()