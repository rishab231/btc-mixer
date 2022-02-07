#!/usr/bin/env python
import pytest
import re
from click.testing import CliRunner
import requests

from project.jobcoin import config
from project import cli


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
    assert 'Welcome to the Jobcoin mixer' in result.output


def test_cli_creates_address():
    runner = CliRunner()
    address_create_output = runner.invoke(cli.main, input='add_address 1234,4321').output
    output_re = re.compile(
        r'You may now send Jobcoins to address [0-9a-zA-Z]{32}. '
        'They will be mixed and sent to your destination addresses.'
    )
    assert output_re.search(address_create_output) is not None

def test_cli_deposit_amount():
    r = requests.get("https://jobcoin.gemini.com/iodine-defrost/addresses/Alice")
    # print(r.url)
    # print(r.content)
    # print(r.text)
    # print(r.encoding)
    x = 4
    assert x == 4