from . import config
import logging
from datetime import datetime, timezone
import time
import numpy as np
import time
from typing import List
import uuid

# Write your Jobcoin API client here.
class JobcoinNetwork:
    """
    Polls the network to check for transactions for any deposit address (tied to an address) on the JobCoinNetwork.
    Throws an exception for insufficient balance (or an address is not found).
    """
    MINTED = "(new)"

    def __init__(self):
        self.mixer = Mixer()
        self.network_minted_coins = 0.0

    def add_addresses(self, addresses: List[str]):
        return self.mixer.get_deposit_address(addresses)

    def evaluate_transaction(self, sender: str, receiver: str, amount: str):
        if sender != "None" and self.mixer.get_balance(sender) < float(amount):
            raise Exception("Insufficient Balance!")
        
        if sender == "None":
            transaction = Transaction(JobcoinNetwork.MINTED, receiver, amount)
            self.network_minted_coins += amount
        else:
            transaction = Transaction(sender, receiver, amount)

        self.mixer.execute_transaction(transaction)

    def get_transactions(self, address=None):
        return self.mixer.get_all_transactions(address)



class Transaction:
    """
    Captures a transaction on the JobCoinNetwork.
    Throws an exception for insufficient balance.
    """
    def __init__(self, fromAddress: str, toAddress: str, amount: str):
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount
        self.timestamp = datetime.now(timezone.utc).isoformat(sep='T')
    
    def get_from_address(self):
        return self.fromAddress
    
    def get_to_address(self):
        return self.toAddress
    
    def get_amount(self):
        return self.toAddress

    def return_transaction(self):
        if not self.fromAddress:
            fromAddressOutput = ""
        else:
            fromAddressOutput = 'fromAddress": "{},'.format(self.fromAddress)

        # if not self.fromAddress:
        #     return """{
        #         "timestamp": "{}",
        #         "toAddress": "{}",
        #         "amount": "{}"
        #     }""".format(self.timestamp, self.toAddress, self.amount)
        # else:
        #     return """{
        #         "timestamp": "{}",
        #         "toAddress": "{}",
        #         "fromAddress": "{}",
        #         "amount": "{}"
        #     }""".format(self.timestamp, self.toAddress, self.fromAddress, self.amount)

        return '{"timestamp": "{}", "toAddress": "{}",{}"amount": "{}"}'.format(self.timestamp, self.toAddress, self.fromAddress, self.amount)


class Wallet:
    """
    A wallet is owned by a user, who provides a unique list of owned addresses.
    """
    def __init__(self, private_addresses: List[str], deposit_address: str):
        self.private_addresses = private_addresses
        self.deposit_address = deposit_address
        self.balance = 0.0
        self.transactions = []

    def get_num_addresses(self):
        return len(self.private_addresses)

    def get_balance(self):
        return self.balance
    
    def increase_balance(self, amount: float):
        self.balance += amount

    def decrease_balance(self, amount: float):
        self.balance -= amount
    
    def get_transaction_history(self):
        return "balance: {}, {}".format(self.balance, [xact.return_transaction() for xact in transactions])


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
        return self.deposit_addresses_to_wallet[address].balance
    
    def get_deposit_address(self, deposit_addresses: List[str]) -> str:
        new_address = uuid.uuid4().hex

        while new_address in self.deposit_addresses_to_wallet:
            new_address = uuid.uuid4().hex
        
        self.deposit_addresses_to_wallet[new_address] = Wallet(deposit_addresses, new_address)
        return new_address
    
    def execute_transaction(self, transaction: Transaction, minted=False):
        sender_address: str = transaction.get_from_address()
        receiver_address: str = transaction.get_from_address()
        amount: float = float(transaction.get_amount())

        fee = amount * self.fee_percentage
        amount_after_fee = amount - fee

        if not minted:
            self._transfer_amount(sender_address, self._house_address, amount_after_fee)

        self._transfer_discrete(receiver_address, amount_after_fee)

        # We also charge the fee for minted transactions
        self.fees_collected += amount * fee
        self.transaction_queue.append(transaction)

    def _transfer_amount(self, sender: str, receiver: str, amt: float):
        if sender != None:
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
    
    def _transfer_discrete(self, receiver: str, amt: float):
        num_addresses_receiver = self.deposit_addresses_to_wallet[receiver]
        random_amounts = np.random.random(num_addresses_receiver)
        random_amounts /= random_amounts.sum()

        random_sleep_times = np.random.randint(low=1, high=8, size=num_addresses_receiver-1)
        self._transfer_amount(self._house_address, receiver, random_amounts[0])

        for i in range(1, len(random_amounts)):
            time.sleep[random_sleep_times[i-1]]
            self._transfer_amount(self._house_address, receiver, random_amounts[i])
        
        return 1

    def get_all_transactions(self, address):
        if address is None:
            return str([xact.return_transaction() for xact in self.transaction_queue])

        elif address not in self.deposit_addresses_to_wallet:
            return []
        
        else:
            return self.deposit_addresses_to_wallet[address].get_transaction_history()