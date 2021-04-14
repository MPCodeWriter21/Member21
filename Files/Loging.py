#!/usr/bin/python3
# Logging
# CodeWriter21

# Imports
from datetime import datetime
from colorama import AnsiToWin32 as AnsiToWin
from .Constants import r
import os, sys, platform

__all__ = ['Logger']


# Logger class
class Logger:
    is_started = False

    def __init__(self):
        self.ATW = AnsiToWin(sys.stdout)
        if 'windows' in platform.system().lower():
            self.write_text = self.ATW.write_and_convert
        else:
            self.write_text = self.ATW.write

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

    def print(self, *args, end='\n'):
        txt = ' '.join(str(a) for a in args) + str(end)
        if txt.startswith(r):
            self.write_text(r + ' ' * os.get_terminal_size()[0] + r)
        now = datetime.now()
        if self.is_started:
            path = os.path.join('Logs', f'PrintLog {now.year}-{now.month}-{now.day} {self.me.id}')
        else:
            path = os.path.join('Logs', f'PublicPrintLog {now.year}-{now.month}-{now.day}')
        f = open(path, 'a')
        f.write(f'[{str(now)}] ' + txt)
        f.close()
        self.write_text(txt)
