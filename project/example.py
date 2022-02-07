#!/usr/bin/env python
import uuid
import sys

import click

from jobcoin import jobcoin


help_string = """
    This Jobcoin Mixer CLI supports the following commands:
        a) add_address address1,[address2,...]                  Add addresses to the JobcoinMixer and allocate a new deposit address
        b) send [sender] [receiver] [amount]                    Send amount from sender to receiver
        c) get_transactions                                     Get all transactions in the JobcoinMixer
        d) get_transactions [address]                           Get all transactions associated with address in the JobcoinMixer
        e) help                                                 See help docstring
        f) blank (enter)                                        Exit from this CLI tool
    """


def main():
    print('Welcome to the Jobcoin mixer!\n')

    network = jobcoin.JobcoinNetwork()

    while True:
        click.prompt(
            'Please enter your command',
            prompt_suffix='\n[blank to quit] > ',
            default='',
            show_default=False)
            
        prompt_runner()

@click.command()
@click.option('--add_address', help='number of greetings')
@click.option('--send', help='send')
@click.option('--get_transactions', default='', help='Get all transactions associated with address in the JobcoinMixer')
@click.option('--help', nargs=0)
def prompt_runner(add_address, send, get_transactions, help):
    is_blank = True

    if help:
        click.echo(help_string)
        return
    if add_address:
        click.echo("Address is {}".format(address))
        is_blank = False
    if send:
        click.echo("Send args are {}".format(send))
        is_blank = False
    if get_transactions:
        click.echo("Get transactions args are {}".format(get_transactions))
        is_blank = False
    
    if is_blank:
        sys.exit(0)


if __name__ == '__main__':
    sys.exit(main())
