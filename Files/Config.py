#!/usr/bin/python3
# Config
# CodeWriter21

from .Functions import *
from .Exceptions import ButtonsNotSetException
import pickle

__all__ = ['Config', 'load_configs']


class Config:
    def __init__(self, config_name: str, creator_name: str, bot_id: str, ads_channel: str, enabled: bool = False,
                 required_channels: list = []):
        self.config_name = config_name
        self.creator_name = creator_name
        self.bot_id = bot_id
        self.ads_channel = ads_channel
        self.required_channels = required_channels
        self.enabled = enabled
        self.channel_link_button = None
        self.submit_button = None
        self.__creation_date = datetime.now()
        self.__edit_dates = []
        self.__edited()

    def set_buttons(self, channel_link_row: int = 1, channel_link_column: int = 1, submit_button_row: int = 1,
                    submit_button_column: int = 0):
        logger.writel(f'Config [{self.config_name}] buttons has setten.')
        self.channel_link_button = (channel_link_row, channel_link_column)
        self.submit_button = (submit_button_row, submit_button_column)
        self.__edited()

    def set_property(self, bot_id: str = '', ads_channel: str = '', required_channels: list = []):
        if bot_id:
            logger.writel(f'Config [{self.config_name}] property(bot_id) has setten.')
            self.bot_id = bot_id
        if ads_channel:
            logger.writel(f'Config [{self.config_name}] property(ads_channel) has setten.')
            self.ads_channel = ads_channel
        if required_channels:
            logger.writel(f'Config [{self.config_name}] property(required_channels) has setten.')
            self.required_channels = required_channels
        self.__edited()

    def set_enabled(self, enabled: bool):
        logger.writel(f'Config [{self.config_name}] property(enabled) is set.')
        self.enabled = enabled

    def Save(self):
        if (not self.channel_link_button) or (not self.submit_button):
            raise ButtonsNotSetException('Buttons Not Set!')
        path = os.path.join('BotConfigs', self.config_name) + '.bco'
        with open(path, 'wb') as file:
            pickle.dump(self, file)
            logger.writel(f'Config [{self.config_name}] saved in "{self.path}".')

    def Load(path):
        with open(path, 'rb') as file:
            return pickle.load(file)

    def get_creation_date(self):
        return self.__creation_date

    def get_last_edit_date(self):
        return self.__last_edit

    def __edited(self):
        logger.writel(f'Config [{self.config_name}] edited.')
        self.__last_edit = datetime.now()
        self.__edit_dates.append(self.__last_edit)


def load_configs():
    from .Constants import logger
    # try:
    if True:
        # Loads configs
        logger.writel("Loading configs...")

        files = os.listdir('BotConfigs')

        config_files = []
        for file in files:
            path = os.path.join('BotConfigs', file)
            if os.path.isfile(path) and file.endswith('.bco'):
                config_files.append(path)

        # Backups configs
        logger.writel("Making a backup of configs...")
        for cnf in config_files:
            Backup(cnf, 'Backup' + str(ttime()) + ' - ' + os.path.split(cnf)[1])
        logger.writel("Backups Made.")
    # except:
    #	logger.writel("Failed!")
    #	config_files = []

    configs = []
    for cnf in config_files:
        config = Config.Load(cnf)
        configs.append(config)

    return configs
