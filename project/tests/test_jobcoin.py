#!/usr/bin/env python
import pytest
import re
from project.jobcoin import jobcoin

@pytest.fixture
def test_address_created():
    network = JobcoinNetwork()
    address_create_output = network.add_addresses(["1234", "5678"])
    output_re = re.compile(
        r'[0-9a-zA-Z]{32}. '
    )
    assert output_re.search(address_create_output) is not None