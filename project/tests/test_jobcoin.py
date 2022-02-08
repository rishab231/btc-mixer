#!/usr/bin/env python
import pytest
import re
from project.jobcoin.jobcoin_network import JobcoinNetwork
from project.jobcoin.exceptions import DepositAddressDoesntExistException, InsufficientBalanceException

@pytest.fixture
def before_all():
    network = JobcoinNetwork()
    deposit_1 = network.add_addresses(["0x4g7z", "0x8a54"])
    amount = '100.0'
    network.send(JobcoinNetwork.MINTED, deposit_1, amount)
    return network, deposit_1, amount

def test_address_created(before_all):
    network, deposit_1, amount = before_all
    address_create_output = network.add_addresses(["0xp45", "0x8a45"])
    output_re = re.compile(
        r'[0-9a-zA-Z]{32}'
    )
    assert output_re.search(address_create_output) is not None

def test_minting(before_all):
    network, deposit_1, amount = before_all
    my_transactions = network.get_transactions(deposit_1)
    assert "'fromAddress': '{}'".format(JobcoinNetwork.MINTED) in my_transactions
    assert "'toAddress': '{}'".format(deposit_1) in my_transactions
    assert "'amount': '{}'".format(amount) in my_transactions
    assert network.get_num_coins_minted() == pytest.approx(float(amount))

def test_simple_send(before_all):
    network, deposit_1, amount_1 = before_all

    deposit_2 = network.add_addresses(["0xf001", "0x200d"])
    amount_2 = "90.0"
    network.send(deposit_1, deposit_2, amount_2)
    account_2_transactions = network.get_transactions(deposit_2)
    assert "'fromAddress': '{}'".format(deposit_1) in account_2_transactions
    assert "'toAddress': '{}'".format(deposit_2) in account_2_transactions
    assert "'amount': '{}'".format(amount_2) in account_2_transactions

    print("Amount 1 is {}".format(amount_1))
    assert network.mixer.get_balance(deposit_1) == pytest.approx((float(amount_1) * (1 - 0.02) - float(amount_2)))
    assert network.mixer.get_balance(deposit_2) == pytest.approx((float(amount_2)) * (1-0.02))

def test_insufficient_balance(before_all):
    network, deposit_1, amount_1 = before_all

    deposit_2 = network.add_addresses(["0xf001", "0x200d"])
    amount_2 = "200.0"

    with pytest.raises(InsufficientBalanceException):
        network.send(deposit_1, deposit_2, amount_2)

def test_sender_address_no_exists():
    network = JobcoinNetwork()
    sender_address = "abc"
    receiver_address = "def"
    with pytest.raises(DepositAddressDoesntExistException):
        network.send(sender_address, receiver_address, '200.0')

def test_receiver_address_no_exists(before_all):
    network, sender_address, amount = before_all
    receiver_address = "0xd7fe"
    with pytest.raises(DepositAddressDoesntExistException):
        network.send(sender_address, receiver_address, '200.0')

def test_balance(before_all):
    network, deposit_1, amount = before_all
    deposit_2 = network.add_addresses(["0xf001", "0x200d"])
    amount_2 = "50.0"
    network.send(deposit_1, deposit_2, amount_2)
    deposit_3 = network.add_addresses(["0x7j4f", "0x20a"])
    amount_3 = "30.0"
    network.send(deposit_1, deposit_3, amount_3)
    print(network.get_transactions(deposit_1))
    assert "balance: 18" in network.get_transactions(deposit_1)
    assert "balance: 49" in network.get_transactions(deposit_2)
    assert "balance: 29.4" in network.get_transactions(deposit_3)
    assert network.get_fees_collected() == pytest.approx((float(amount) + float(amount_2) + float(amount_3)) * 0.02)