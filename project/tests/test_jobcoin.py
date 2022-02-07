#!/usr/bin/env python
import pytest
import re
from project.jobcoin import jobcoin

@pytest.fixture
def before_all():
    network = jobcoin.JobcoinNetwork()
    deposit_1 = network.add_addresses(["1234", "5678"])
    amount = '100.0'
    network.send("None", deposit_1, amount)
    return network, deposit_1, amount

def test_address_created(before_all):
    network, deposit_1, amount = before_all
    address_create_output = network.add_addresses(["8010", "3096"])
    output_re = re.compile(
        r'[0-9a-zA-Z]{32}'
    )
    assert output_re.search(address_create_output) is not None

def test_minting(before_all):
    network, deposit_1, amount = before_all
    my_transactions = network.get_transactions(deposit_1)
    assert "'fromAddress': '{}'".format(jobcoin.JobcoinNetwork.MINTED) in my_transactions
    assert "'toAddress': '{}'".format(deposit_1) in my_transactions
    assert "'amount': '{}'".format(amount) in my_transactions
    assert network.get_num_coins_minted() == float(amount)

def test_simple_send(before_all):
    network, deposit_1, amount_1 = before_all

    deposit_2 = network.add_addresses(["1001", "2002"])
    amount_2 = "90.0"
    network.send(deposit_1, deposit_2, amount_2)
    account_2_transactions = network.get_transactions(deposit_2)
    assert "'fromAddress': '{}'".format(deposit_1) in account_2_transactions
    assert "'toAddress': '{}'".format(deposit_2) in account_2_transactions
    assert "'amount': '{}'".format(amount_2) in account_2_transactions

    print("Amount 1 is {}".format(amount_1))
    assert network.mixer.get_balance(deposit_1) == pytest.approx((float(amount_1) - float(amount_2)) * (1-0.02))
    assert network.mixer.get_balance(deposit_2) == pytest.approx((float(amount_2)) * (1-0.02))

def test_insufficient_balance(before_all):
    network, deposit_1, amount_1 = before_all

    deposit_2 = network.add_addresses(["1001", "2002"])
    amount_2 = "200.0"

    with pytest.raises(jobcoin.InsufficientBalanceException):
        network.send(deposit_1, deposit_2, amount_2)