#!/usr/bin/env python
import uuid
import sys

import click

from jobcoin import jobcoin


@click.command()
@click.option('--add-address', help='number of greetings')
@click.option('--send', help='number of greetings')
@click.option('--get_transactions', default='', help='Get all transactions associated with address in the JobcoinMixer')
@click.option('--help', help='See help docstring')
@click.option('--blank', help='Exit from CLI tool')
def main(args=None):
    print('Welcome to the Jobcoin mixer!\n')

    help_string = """
    This Jobcoin Mixer CLI supports the following commands:
        a) add_address address1,[address2,...]                  Add addresses to the JobcoinMixer and allocate a new deposit address
        b) send [sender] [receiver] [amount]                    Send amount from sender to receiver
        c) get_transactions                                     Get all transactions in the JobcoinMixer
        d) get_transactions [address]                           Get all transactions associated with address in the JobcoinMixer
        e) help                                                 See help docstring
        f) blank (enter)                                        Exit from this CLI tool
    """

    network = jobcoin.JobcoinNetwork()

    while True:
        input_ = click.prompt(
            'Please enter your command',
            prompt_suffix='\n[blank to quit] > ',
            default='',
            show_default=False)

        if input_.strip() == '':
            sys.exit(0)

        command, args = input_.split(' ', 1)
        if command == "add_address":
            args = args.replace(' ', '')
            addresses = args[1].split(",")
            deposit_address = network.add_addresses(addresses)
            click.echo(
            '\nYou may now send Jobcoins to address {deposit_address}. They '
            'will be mixed and sent to your destination addresses.\n'
              .format(deposit_address=deposit_address))
        
        else:
            click.echo(help_string)

# @click.command()
# @click.option('--n', default=1)
# def prompt_runner(command, arguments):


if __name__ == '__main__':
    sys.exit(main())
