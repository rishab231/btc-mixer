#!/usr/bin/env python
from unicodedata import decomposition
import pytest
import re
from project.jobcoin import jobcoin

def test_address_created():
    network = jobcoin.JobcoinNetwork()
    address_create_output = network.add_addresses(["1234", "5678"])
    output_re = re.compile(
        r'[0-9a-zA-Z]{32}'
    )
    assert output_re.search(address_create_output) is not None

def test_minting():
    network = jobcoin.JobcoinNetwork()
    deposit_1 = network.add_addresses(["1234", "5678"])
    amount = '100.0'
    print(deposit_1)
    #deposit_2 = network.add_addresses(["1001", "2002"])
    network.send("None", deposit_1, amount)
    my_transactions = network.get_transactions(deposit_1)
    assert "'fromAddress': '(new)'" in all_transactions
    assert "'toAddress': '{}'".format(deposit_1) in all_transactions
    assert "'amount': '{}'".format(amount) in all_transactions

def test_simple_send():
    network = jobcoin.JobcoinNetwork()
    deposit_1 = network.add_addresses(["1234", "5678"])
    deposit_2 = network.add_addresses(["1001", "2002"])
    amount = '200.0'

    network.send("None", deposit_1, amount)
    network.send(deposit_1, deposit_2, amount)
    
    all_transactions = network.get_transactions()
    assert "'fromAddress': '{}'".format(deposit_1) in all_transactions
    assert "'toAddress': '{}'".format(deposit_2) in all_transactions
    assert "'amount': '{}'".format(amount) in all_transactions