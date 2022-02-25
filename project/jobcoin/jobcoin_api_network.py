from project.jobcoin.transaction import Transaction
from . import config
from typing import List, Optional
from project.jobcoin.mixer import APIBasedMixer
from project.jobcoin.exceptions import DepositAddressDoesntExistException, InsufficientBalanceException

class JobcoinAPINetwork:
    """
    User-facing network class that interacts with the user's input.
    """
    MINTED = "(new)"

    def __init__(self):        
        self.mixer = APIBasedMixer()

    def add_addresses(self, addresses: List[str]) -> str:
        """
        Adds a list of addresses to the network and assigns a deposit address.

        Args:
            addresses (List[str]): A list of user's private addresses

        Returns:
            str: Unique deposit address allocated by Mixer
        """        
        return self.mixer.get_deposit_address(addresses)

    def send(self, sender: str, receiver: str, amount: str) -> Optional[str]:
        """
        Send an amount from sender to receiver.

        Args:
            sender (str): Sender's deposit address
            receiver (str): Receiver's deposit address
            amount (str): Amount to be sent

        Raises:
            DepositAddressDoesntExistException: If sender's or receiver's deposit address doesn't exist in Mixer.
            InsufficientBalanceException: If sender has insufficient balance to cover amount.
        """                    
        is_minted = sender == JobcoinAPINetwork.MINTED
        response = self.mixer.execute_transaction(sender, receiver, amount, is_minted)
        return response

    def get_transactions(self, address=None) -> str:
        """
        Returns a list of transactions associated with a given deposit address.
        If address is None, get all transactions in Mixer.

        Args:
            address ([type], optional): Deposit address associated with a wallet. Defaults to None.

        Returns:
            str: A balance and list of transactions associated with address as JSON string. If no address, get all transactions from mixer.
        """        
        return self.mixer.get_transactions(address)

    def get_fees_collected(self) -> float:
        """
        Returns amount of fees that the Mixer has collected so far

        Returns:
            float: Fees collected so far
        """        
        return self.mixer.get_fees_collected()