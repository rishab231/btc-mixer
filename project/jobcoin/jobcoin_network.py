from project.jobcoin.transaction import Transaction
from . import config
from typing import List
from project.jobcoin.mixer import Mixer
from project.jobcoin.exceptions import DepositAddressDoesntExistException, InsufficientBalanceException

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

    def send(self, sender: str, receiver: str, amount: str):
        if sender != JobcoinNetwork.MINTED and not self.mixer.contains_key(sender):
            raise DepositAddressDoesntExistException(sender)
        if not self.mixer.contains_key(receiver):
            raise DepositAddressDoesntExistException(receiver)
        if self.mixer.get_balance(sender) < float(amount):
            raise InsufficientBalanceException()
        
        if sender == JobcoinNetwork.MINTED:
            self.mint_coins(amount)
            
        transaction = Transaction(sender, receiver, amount)
        is_minted = sender == JobcoinNetwork.MINTED
        self.mixer.execute_transaction(transaction, is_minted)

    def get_transactions(self, address=None):
        return self.mixer.get_transactions(address)

    def mint_coins(self, amount: str):
        self.network_minted_coins += float(amount)

    def get_num_coins_minted(self):
        return self.network_minted_coins