#!/usr/bin/env python
import pytest
import re
from click.testing import CliRunner
import requests

from project.jobcoin import config
from project import cli
from project.jobcoin.exceptions import DepositAddressDoesntExistException


@pytest.fixture
def response():
    import requests
    return requests.get('https://jobcoin.gemini.com/')


def test_content(response):
    assert 'Hello!' in response.content.decode('utf-8')


def test_cli_basic():
    runner = CliRunner()
    result = runner.invoke(cli.main)

    assert result.exit_code == 0
    assert 'Welcome to the Jobcoin network' in result.output


def test_cli_creates_address():
    runner = CliRunner()
    address_create_result = runner.invoke(cli.main, input='add_address 0x4g7z,0x8a54')
    output_re = re.compile(
        r'You may now send Jobcoins to address [0-9a-zA-Z]{32}. '
        'They will be mixed and sent to your destination addresses.'
    )

    assert address_create_result.exit_code == 0
    assert output_re.search(address_create_result.output) is not None

def test_cli_send_failure():
    runner = CliRunner()
    deposit_address = '0x4t'
    result = runner.invoke(cli.main, input='send {} 100'.format(deposit_address))

    assert result.exit_code == 0
    assert 'Deposit address ({}) does not exist in the JobMixer'.format(deposit_address) in result.output

def test_cli_value_error():
    runner = CliRunner()
    deposit_address = '0x4t'
    result = runner.invoke(cli.main, input='send {}'.format(deposit_address))

    assert result.exit_code == 0
    assert 'Malformed input! Type help for usage.'.format(deposit_address) in result.output

def test_cli_command_error():
    runner = CliRunner()
    deposit_address = '0x4t'
    result = runner.invoke(cli.main, input='foo {}'.format(deposit_address))
    assert result.exit_code == 0
    assert 'Command not found! Type help for usage.'.format(deposit_address) in result.output

def test_cli_blank_input_exits():
    runner = CliRunner()
    address_create_result = runner.invoke(cli.main, input='\n add_address 0x4g7z,0x8a54')
    output_re = re.compile(
        r'You may now send Jobcoins to address [0-9a-zA-Z]{32}. '
        'They will be mixed and sent to your destination addresses.'
    )

    assert address_create_result.exit_code == 0
    assert output_re.search(address_create_result.output) is None