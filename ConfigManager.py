#!/usr/bin/python3
# Configures Telegram API
# CodeWriter21

# Imports
from Files.Functions import *
from Files.Config import *

# Makes needed directories
mkdirs()
logger.writel('Needed directories made.')


def main():
    logger.writel('Loading configs.')
    # Gets configs
    configs = load_configs()
    logger.writel('Configs loaded.')

    print(banner)
    print(p + colors.Green + 'Avalable Configs ' + co)
    if len(configs) > 0:
        for cnf in configs:
            print(colors.Red + '          ' + cnf.config_name + end)
            print(a + colors.Blue + 'Creator: ' + cnf.creator_name + end)
            print(a + colors.Blue + 'Bot-id : ' + cnf.bot_id + end)
            print(a + colors.Blue + 'Status : ' +
                  (colors.Green + 'Enabled' if cnf.enabled else colors.Red + 'Disabled') + end)
            print('\n')
    else:
        print(n + colors.Red + 'Nothing );')
        print('\n')
    logger.writel("Configs Data printed.")

    options = ['1']
    print(a + colors.Green + 'Options' + co)
    print(f'{colors.Yellow}[{colors.Green}1{colors.Yellow}] {colors.Blue}Create A New Config')
    if len(configs) > 0:
        options.append('2')
        print(f'{colors.Yellow}[{colors.Green}2{colors.Yellow}] {colors.Blue}Delete An Exiting Config')
        options.append('3')
        print(f'{colors.Yellow}[{colors.Green}3{colors.Yellow}] {colors.Blue}Edit An Exiting Config')
    if len(options) > 1:
        while True:
            option = input(a + colors.Pink + 'Choose Option ' + co + ' ' + colors.Cyan)
            if option in options:
                break
    else:
        option = '1'

    logger.writel('Option ' + option + ' has choosen.')

    clear()
    print(banner)

    if option == '1':
        logger.writel('Creating a new config...')
        print(p + colors.Red + 'Create Your New Config ;)' + end)

        config_name = creator_name = bot_id = ads_channel = channel_id = ''
        required_channels = []
        while not config_name:
            config_name = input(a + colors.Green + 'Please enter a name for config ' + co + ' ' + colors.Cyan)
        creator_name = input(a + colors.Blue + 'Enter your name or nickname    ' + co + ' ' + colors.Cyan)
        while not bot_id:
            bot_id = input(a + colors.Green + 'Please enter Telegram Bot ID   ' + co + ' ' + colors.Cyan)
        while not ads_channel:
            ads_channel = input(a + colors.Green + 'Please enter ads-channel ID    ' + co + ' ' + colors.Cyan)
        required_channels = []
        while True:
            channel_id = input(
                a + colors.Green + f'Please enter ID of required channels to join{colors.Red}({colors.Cyan}Enter END when finished{colors.Red}) ' + co + ' ' + colors.Cyan)
            if channel_id.lower() == 'end':
                break
            if channel_id:
                required_channels.append(channel_id)

        options = ['m', 'd']
        while not option in options:
            option = input(
                a + colors.Pink + f'Do you want to setup buttons {colors.Green}M{colors.Pink}anually or use {colors.Red}D{colors.Pink}efault settings?(M/D) ' + co + ' ' + colors.Cyan).lower()

        config = Config(config_name, creator_name, bot_id, ads_channel, True, required_channels)

        if option == 'd':
            config.set_buttons()
        else:
            channel_link_row = ''
            channel_link_column = ''
            submit_button_row = ''
            submit_button_column = ''
            while not channel_link_row.isdigit():
                channel_link_row = input(
                    a + colors.Yellow + 'Enter row of the button whitch contains channel link to join(Starting from 0 in top)     ' + co + ' ' + colors.Cyan)
            while not channel_link_column.isdigit():
                channel_link_column = input(
                    a + colors.Yellow + 'Enter column of the button whitch contains channel link to join(Starting from 0 in left) ' + co + ' ' + colors.Cyan)
            while not submit_button_row.isdigit():
                submit_button_row = input(
                    a + colors.Yellow + 'Enter row of the button whitch you click to submit(Starts from 0 in top)     ' + co + ' ' + colors.Cyan)
            while not submit_button_column.isdigit():
                submit_button_column = input(
                    a + colors.Yellow + 'Enter column of the button whitch you click to submit(Starts from 0 in left) ' + co + ' ' + colors.Cyan)
            config.set_buttons(int(channel_link_row), int(channel_link_column), int(submit_button_row),
                               int(submit_button_column))

        logger.writel('Saving new config...')
        config.Save()
        logger.writel('Config saved.')
    else:
        if len(configs) > 1:
            i = 1
            for config in configs:
                print(
                    a + f'{colors.Yellow}({colors.Pink}{i}{colors.Yellow}) {colors.Cyan}{config.config_name}{colors.Gray}({config.bot_id})' +
                    (
                        f' {colors.White}by {colors.Blue} {config.creator_name}' if config.creator_name else '') + f'\t {colors.White}Status{co} ' +
                    (f'{colors.Green}Enabled' if config.enabled else f'{colors.Red}Disabled') + end)
                i += 1
            options = range(1, len(configs) + 1)
        if option == '2':
            logger.writel('Deleting config...')
            if len(configs) > 1:
                while True:
                    option = input(
                        a + colors.Pink + f'Choose number of Config to {colors.Red}DELETE {colors.Gray}(C to cancell)' + co + ' ' + colors.Cyan)
                    if option.lower() == 'c':
                        logger.writel('Cancelled!')
                        print(a + colors.Pink + 'Cancelled!' + end)
                        Exit()
                    if option.isdigit() and int(option) in options:
                        break
            else:
                option = 1
            config = configs[int(option) - 1]
            sure = input(
                a + colors.Red + f'Are you sure you want to {end + colors.BackRed}DELETE{end + colors.Red} this Config({config.config_name})?{colors.Yellow}({colors.Red}y{colors.Yellow}/{colors.Green}N{colors.Yellow}) ' + colors.Cyan)
            if sure.lower() == 'y':
                logger.writel('Removing config...')
                os.remove(config.path)
                logger.writel(f'Config [{config.path}] removed!')
                print(n + colors.Red + f'Config({config.config_name}) removed!' + end)
                Exit()
        else:
            if len(configs) > 1:
                while True:
                    option = input(
                        a + colors.Pink + f'Choose number of Config to {colors.Yellow}EDIT {colors.Gray}(C to cancell)' + co + ' ' + colors.Cyan)
                    if option.lower() == 'c':
                        print(a + colors.Red + 'Cancelled!' + end)
                        Exit()
                    if option.isdigit() and int(option) in options:
                        break
            else:
                option = 1
            config = configs[int(option) - 1]
            print(colors.White + 'Config Name       ' + co + ' ' + colors.BCyan + config.config_name + end)
            if config.creator_name:
                print(colors.White + 'Creator           ' + co + ' ' + colors.Green + config.creator_name + end)
            print(colors.White + 'Bot ID            ' + co + ' ' + colors.Blue + config.bot_id + end)
            print(colors.White + 'Ads-Channel       ' + co + ' ' + colors.Blue + config.ads_channel + end)
            if config.required_channels:
                print(
                    colors.White + 'Required Channels ' + co + ' ' + colors.Blue + str(config.required_channels) + end)
            print(colors.White + 'Buttons           ' + co + ' ' + end)
            print(colors.Blue + 'Link   Button     ' + co + ' ' + colors.Pink + str(config.channel_link_button) + end)
            print(colors.Blue + 'Submit Button     ' + co + ' ' + colors.Pink + str(config.submit_button) + end)
            print(colors.White + 'Creation Date     ' + co + ' ' + colors.Blue + str(config.get_creation_date()) + end)
            print(colors.White + 'Last Edit Date    ' + co + ' ' + colors.Blue + str(config.get_last_edit_date()) + end)
            print(colors.White + 'Status            ' + co + ' ' + (
                f'{colors.Green}Enabled' if config.enabled else f'{colors.Red}Disabled') + end)

            while True:
                print()
                print(a + colors.Blue + colors.BackGreen + 'OPTIONS' + end + ' ' + co + end)
                print(f'{colors.Yellow}({colors.Pink}1{colors.Yellow}) {colors.Blue}Edit Bot ID' + end)
                print(f'{colors.Yellow}({colors.Pink}2{colors.Yellow}) {colors.Blue}Edit Ads-Channel' + end)
                print(f'{colors.Yellow}({colors.Pink}3{colors.Yellow}) {colors.Blue}Edit Required Channels' + end)
                print(f'{colors.Yellow}({colors.Pink}4{colors.Yellow}) {colors.Blue}Edit Buttons' + end)
                print(f'{colors.Yellow}({colors.Pink}5{colors.Yellow}) {colors.Blue}Edit Status' + end)
                print(f'{colors.Yellow}({colors.Pink}0{colors.Yellow}) {colors.Red }Exit' + end)

                options = ['0', '1', '2', '3', '4', '5']
                while True:
                    option = input(a + colors.Pink + 'Choose Option ' + co + ' ' + colors.Cyan)
                    if option in options:
                        break
                option = int(option)

                if option == 0:
                    break
                elif option == 1:
                    new_bot_id = input(a + colors.Pink + 'Enter New Bot ID ' + colors.Yellow +
                                       f'[{colors.Pink}Default {co} {colors.Blue + config.bot_id + colors.Yellow}]' + co + colors.Cyan)
                    if not new_bot_id: new_bot_id = config.bot_id
                    config.set_property(bot_id=new_bot_id)
                    config.Save()
                    print(p + colors.Green + 'Bot-ID set!' + end)
                elif option == 2:
                    new_channel = input(a + colors.Pink + 'Enter New Ads-Channel ' + colors.Yellow +
                                        f'[{colors.Pink}Default {co} {colors.Blue + config.ads_channel + colors.Yellow}]' + co + colors.Cyan)
                    if not new_channel: new_channel = config.ads_channel
                    config.set_property(ads_channel=new_channel)
                    config.Save()
                    print(p + colors.Green + 'Ads-Channel set!' + end)
                elif option == 3:
                    new_required_channels = []
                    while True:
                        channel_id = input(
                            a + colors.Pink + f'Please enter ID of required channels to join{colors.Red}({colors.Cyan}Enter END when finished{colors.Red}) ' + co + ' ' + colors.Cyan)
                        if channel_id.lower() == 'end':
                            break
                        if channel_id:
                            new_required_channels.append(channel_id)
                    config.set_property(required_channels=new_required_channels)
                    config.Save()
                    print(p + colors.Green + 'Required Channels set!' + end)
                elif option == 4:
                    channel_link_row = channel_link_column = submit_button_row = submit_button_column = ''
                    while not channel_link_row.isdigit():
                        channel_link_row = input(
                            a + colors.Yellow + 'Enter row of the button whitch contains channel link to join(Starting from 0 in top) ' +
                            f'[Default {co} {colors.Blue + str(config.channel_link_button[0]) + colors.Yellow}]' + co + ' ' + colors.Cyan)
                        if not channel_link_row:     channel_link_row = str(config.channel_link_button[0])
                    while not channel_link_column.isdigit():
                        channel_link_column = input(
                            a + colors.Yellow + 'Enter column of the button whitch contains channel link to join(Starting from 0 in left) ' +
                            f'[Default {co} {colors.Blue + str(config.channel_link_button[1]) + colors.Yellow}]' + co + ' ' + colors.Cyan)
                        if not channel_link_column:  channel_link_column = str(config.channel_link_button[1])
                    while not submit_button_row.isdigit():
                        submit_button_row = input(
                            a + colors.Yellow + 'Enter row of the button whitch you click to submit(Starts from 0 in top) ' +
                            f'[Default {co} {colors.Blue + str(config.submit_button[0]) + colors.Yellow}]' + co + ' ' + colors.Cyan)
                        if not submit_button_row:    submit_button_row = str(config.submit_button[0])
                    while not submit_button_column.isdigit():
                        submit_button_column = input(
                            a + colors.Yellow + 'Enter column of the button whitch you click to submit(Starts from 0 in left) ' +
                            f'[Default {co} {colors.Blue + str(config.submit_button[1]) + colors.Yellow}]' + co + ' ' + colors.Cyan)
                        if not submit_button_column: submit_button_column = str(config.submit_button[1])
                    config.set_buttons(int(channel_link_row), int(channel_link_column), int(submit_button_row),
                                       int(submit_button_column))
                    config.Save()
                    print(p + colors.Green + 'Buttons set!' + end)
                elif option == 5:
                    if config.enabled:
                        option = input(
                            a + colors.Pink + f'Do you want to disable this config?{colors.Yellow}({colors.Red}Y{colors.Yellow}/{colors.Green}N{colors.Yellow}) ' + co + ' ' + colors.Cyan)
                        if option.lower() == 'y':
                            config.set_enabled(False)
                            config.Save()
                            print(p + colors.Red + 'Config disabled!' + end)
                        else:
                            print(n + colors.Yellow + 'Disabling cancelled!' + end)
                    elif not config.enabled:
                        option = input(
                            a + colors.Pink + f'Do you want to enable this config?{colors.Yellow}({colors.Green}Y{colors.Yellow}/{colors.Red}N{colors.Yellow}) ' + co + ' ' + colors.Cyan)
                        if option.lower() == 'y':
                            config.set_enabled(True)
                            config.Save()
                            print(p + colors.Green + 'Config enabled!' + end)
                        else:
                            print(n + colors.Yellow + 'Enabling cancelled!' + end)

    Exit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.writel("Canceled: KeyboardInterrupt!")
        print(r + n + colors.Red + "Cancelled!" + end)
        Exit()
