from typing import List

from project.jobcoin.transaction import Transaction

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
        print("Increase balance by {}".format(amount))
        self.balance += amount

    def decrease_balance(self, amount: float):
        self.balance -= amount
    
    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
    
    def get_transaction_history(self):
        print(self.transactions[0].return_transaction())
        return "balance: {}, {}".format(self.balance, [xact.return_transaction() for xact in self.transactions])