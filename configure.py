#!/usr/bin/python3
# Configures Telegram API
# CodeWriter21

# Imports
from Files.Functions import *

# Makes needed directories
mkdirs()


def main():
    # Gets API information from config file
    try:
        # Tries to extract API
        logger.writel("Trying to extract API...")
        api_id, api_hash = get_api()
        logger.writel("API extracted.")

        # Backups last config
        logger.writel("Making a backup of last config...")
        Backup('config', 'Backup' + str(ttime()) + ' - config')
        logger.writel("config backup Made.")
    except:
        logger.writel("Failed!")
        api_id = 0
        api_hash = 'None'

    print(banner)
    print(p + colors.Green + 'Current API Data ' + co)
    print(p + colors.Blue + 'API-ID           ' + co + ' ' + colors.Red + str(api_id))
    print(p + colors.Blue + 'API-HASH         ' + co + ' ' + colors.Red + api_hash)
    print('\n')
    logger.writel("API Data printed.")

    logger.writel("Getting new API Data...")
    new_api_id = input(a + colors.Blue + 'Enter New API-ID  (Default: ' + str(api_id) + ')' + co + ' ' + colors.Green)
    if not new_api_id: new_api_id = api_id
    try:
        new_api_id = int(new_api_id)
    except ValueError:
        print(n + colors.Red + 'API-ID must be a number!' + end)
        Exit()

    new_api_hash = input(a + colors.Blue + 'Enter New API-HASH(Default: ' + api_hash + ')' + co + ' ' + colors.Green)
    if not new_api_hash: new_api_hash = api_hash

    logger.writel("Setting new API...")
    set_api(new_api_id, new_api_hash)
    print(p + colors.Green + 'Done!' + end)
    logger.writel("New API set.")

    Exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.writel("Canceled: KeyboardInterrupt!")
        print(r + n + colors.Red + "Cancelled!" + end)
        Exit()
