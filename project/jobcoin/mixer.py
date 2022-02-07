from project.jobcoin.transaction import Transaction
from project.jobcoin.wallet import Wallet
import logging
import time
import numpy as np
import time
from typing import List
import uuid

class Mixer:
    """
    - [DONE] Provides a new deposit address that it owns.
    - [DONE] Transfers your bitcoins from the deposit address to the house account
    - [DONE] Over time, these bitcoins are transferred in discrete investments to the withdrawal addresses provided, after capturing a 2% fee.
    """
    def __init__(self, fee_percentage: float = 0.02):
        self.deposit_addresses_to_wallet = dict()
        self._house_address = uuid.uuid4().hex
        self.fee_percentage = fee_percentage
        self.house_balance = 0.0
        self.fees_collected = 0.0
        self.transaction_queue = []
    
    def get_balance(self, address):
        if address not in self.deposit_addresses_to_wallet:
            return 0
        print("Balance is", self.deposit_addresses_to_wallet[address].get_balance())
        return self.deposit_addresses_to_wallet[address].get_balance()
    
    def get_deposit_address(self, deposit_addresses: List[str]) -> str:
        new_address = uuid.uuid4().hex

        while new_address in self.deposit_addresses_to_wallet:
            new_address = uuid.uuid4().hex
        
        self.deposit_addresses_to_wallet[new_address] = Wallet(deposit_addresses, new_address)
        return new_address
    
    def execute_transaction(self, transaction: Transaction, is_minted: bool = False):
        sender_address: str = transaction.get_from_address()
        receiver_address: str = transaction.get_to_address()
        amount: float = float(transaction.get_amount())

        fee = amount * self.fee_percentage
        amount_after_fee = amount - fee
        print("Amount after fee {}".format(amount_after_fee))

        self._transfer_amount(sender_address, self._house_address, amount_after_fee, is_minted)
        self._transfer_discrete(receiver_address, amount_after_fee)

        # We also charge the fee for minted transactions
        self.fees_collected += amount * fee
        self.transaction_queue.append(transaction)

        if not is_minted:
            self.deposit_addresses_to_wallet[sender_address].add_transaction(transaction)

        self.deposit_addresses_to_wallet[receiver_address].add_transaction(transaction)

    def _transfer_amount(self, sender: str, receiver: str, amt: float, is_minted: bool):
        if not is_minted:
            if sender == self._house_address:
                self.house_balance -= amt
            else:
                sender_wallet = self.deposit_addresses_to_wallet[sender]
                sender_wallet.decrease_balance(amt)

        if receiver == self._house_address:
            self.house_balance += amt
        else:
            receiver_wallet = self.deposit_addresses_to_wallet[receiver]
            receiver_wallet.increase_balance(amt)

        return 1

    def _get_n_random_proportions(self, n):
        random_props = np.random.random(n-1)
        random_props = (random_props/random_props.sum()).round(2)
        random_props = np.append(random_props, 1.0 - random_props.sum())
        return random_props
    
    def _transfer_discrete(self, receiver: str, amt: float):
        num_addresses_receiver = self.deposit_addresses_to_wallet[receiver].get_num_addresses()
        print("Num addresses receiver", num_addresses_receiver)
        n_random_proportions = self._get_n_random_proportions(num_addresses_receiver)
        print(n_random_proportions)
        print(n_random_proportions.sum())

        random_sleep_times = np.random.randint(low=0, high=1, size=num_addresses_receiver-1)
        self._transfer_amount(self._house_address, receiver, n_random_proportions[0] * amt, is_minted=False)

        for i in range(1, len(n_random_proportions)):
            time.sleep(random_sleep_times[i-1])
            self._transfer_amount(self._house_address, receiver, n_random_proportions[i] * amt, is_minted=False)
        
        return 1

    def contains_key(self, address: str):
        return address in self.deposit_addresses_to_wallet

    def get_transactions(self, address: str):
        if address == None:
            return str([xact.return_transaction() for xact in self.transaction_queue])

        elif address not in self.deposit_addresses_to_wallet:
            return []
        
        else:
            return self.deposit_addresses_to_wallet[address].get_transaction_history()