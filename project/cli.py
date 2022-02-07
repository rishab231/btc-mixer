#!/usr/bin/env python
import uuid
import sys

import click

from jobcoin import jobcoin


@click.command()
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

        if "add_address" in input_:
            command, args = input_.split(' ', 1)
            addresses = args.replace(' ', '')[1].split(",")
            deposit_address = network.add_addresses(addresses)
            click.echo(
            '\nYou may now send Jobcoins to address {deposit_address}. They '
            'will be mixed and sent to your destination addresses.\n'
              .format(deposit_address=deposit_address))
        
        elif "send" in input_:
            command, args = input_.split(' ', 1)
            sender, receiver, amount = args.split(' ')
            network.evaluate_transaction(sender, receiver, amount)
            click.echo(
            '\n{amount} sent from {sender} to {receiver} via JobcoinMixer.\n'
              .format(amount=amount, sender=sender, receiver=receiver))
        
        elif "get_transactions" in input_:
            output = input_.split(' ')
            if len(output) == 1:
                click.echo(network.get_transactions())
            else:
                click.echo(network.get_transactions(output[2]))

        else:
            click.echo(help_string)


if __name__ == '__main__':
    sys.exit(main())
