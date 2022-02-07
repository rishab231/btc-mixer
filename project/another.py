@click.group()
def cli():
    pass

@cli.command()
@cli.option('--add_address', help='number of greetings')
def add_address(add_address):
    click.echo('Address')
    os.system('curl http://127.0.0.1:5000/create')

@cli.command()
def conn():
    click.echo('conn called')
    os.system('curl http://127.0.0.1:5000/')

def main():
    print('Welcome to the Jobcoin mixer!\n')

    network = jobcoin.JobcoinNetwork()

    while True:
        input_ = click.prompt(
                'Please enter your command',
                prompt_suffix='\n[blank to quit] > ',
                default='',
                show_default=False)

        if input_.strip() == '':
            sys.exit(0)

        cli.commands[input_](network)