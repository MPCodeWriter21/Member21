# Python3
# Loging
# CodeWriter21

# Imports
from datetime import datetime
from .Constants import *
import os

# Logger class
class log:
	is_started = False
	def start(self, me):
		self.me = me
		self.new_line()
		self.write('Stareted')
		self.is_started = True

	def new_line(self):
		now = datetime.now()
		if self.is_started:
			path = os.path.join('Logs', f'log {now.year}-{now.month}-{now.day} {self.me.id}')
		else:
			path = os.path.join('Logs', f'PublicLog {now.year}-{now.month}-{now.day}')
		f = open(path, 'a')
		f.write('\n')
		f.close()

	def write(self, text):
		now = datetime.now()
		if self.is_started:
			path = os.path.join('Logs', f'log {now.year}-{now.month}-{now.day} {self.me.id}')
		else:
			path = os.path.join('Logs', f'PublicLog {now.year}-{now.month}-{now.day}')
		f = open(path, 'a')
		f.write(f'[{str(now)}] ' + text)
		f.close()

	def writel(self, text):
		self.write(text)
		self.new_line()

	def print(self, *args, end = '\n'):
		txt = ' '.join(str(a) for a in args) + str(end)
		now = datetime.now()
		if self.is_started:
			path = os.path.join('Logs', f'PrintLog {now.year}-{now.month}-{now.day} {self.me.id}')
		else:
			path = os.path.join('Logs', f'PublicPrintLog {now.year}-{now.month}-{now.day}')
		f = open(path, 'a')
		f.write(f'[{str(now)}] ' + txt)
		f.close()
		print(*args, end = end)