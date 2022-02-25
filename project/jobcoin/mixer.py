import random
from project.jobcoin.transaction import Transaction
from project.jobcoin.wallet import Wallet
import logging
import time
import time
from typing import List, Optional
import uuid
import requests

class Mixer:
    """
    A class that simulates the JobcoinMixer.
    """
    def __init__(self, fee_percentage: float = 0.02):
        """
        Initialize the mixer with a fee percentage

        Args:
            fee_percentage (float, optional): Percentage fee to charge per transaction. Defaults to 0.02.
        """                
        self.deposit_addresses_to_wallet = dict()
        self._house_address = uuid.uuid4().hex
        self.fee_percentage = fee_percentage
        self.house_balance = 0.0
        self.fees_collected = 0.0
        self.transaction_queue = []
    
    def get_balance(self, address: str) -> float:
        """
        Get balance associated with given deposit address.
        If address does not exist in mixer, return 0.

        Args:
            address (str): Deposit address associated with wallet

        Returns:
            float: Balance in wallet associated with deposit address
        """        
        if address not in self.deposit_addresses_to_wallet:
            return 0
        return self.deposit_addresses_to_wallet[address].get_balance()
    
    def get_deposit_address(self, private_addresses: List[str]) -> str:
        """
        Get a fresh deposit address from Mixer.

        Args:
            deposit_addresses (List[str]): A list of private addresses.

        Returns:
            str: A unique deposit address associated with user's wallet
        """        
        new_address = uuid.uuid4().hex

        while new_address in self.deposit_addresses_to_wallet:
            new_address = uuid.uuid4().hex
        
        self.deposit_addresses_to_wallet[new_address] = Wallet(private_addresses, new_address)
        return new_address
    
    def execute_transaction(self, transaction: Transaction, is_minted: bool = False) -> None:
        """
        Execute a transaction through the JobcoinMixer.

        Args:
            transaction (Transaction): A valid transaction initiated.
            is_minted (bool, optional): Whether the transaction involvde the coins minted i.e. no sender. Defaults to False.
        """        
        sender_address: str = transaction.get_from_address()
        receiver_address: str = transaction.get_to_address()
        amount: float = float(transaction.get_amount())

        fee = amount * self.fee_percentage
        amount_after_fee = amount - fee

        # We also charge the fee for minted transactions
        self._transfer_amount(sender_address, self._house_address, amount, is_minted)
        self._transfer_discrete(receiver_address, amount_after_fee)
        
        # Global queue of transactions
        self.transaction_queue.append(transaction)

        if not is_minted:
            self.deposit_addresses_to_wallet[sender_address].add_transaction(transaction)

        self.deposit_addresses_to_wallet[receiver_address].add_transaction(transaction)
        self.fees_collected += fee
        self.house_balance -= fee

    def _transfer_amount(self, sender: str, receiver: str, amt: float, is_minted: bool) -> None:
        """
        Transfers an amount from sender to receiver directly. Sender could be house_address.
        If is_minted, receiver receives balance from network.

        Args:
            sender (str): Sender's deposit address. Could be '(new)' if is_minted.
            receiver (str): Receiver's deposit address.
            amt (float): Amount.
            is_minted (bool): If coins were minted from network.
        """        
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


    def _get_n_random_proportions(self, n) -> List[float]:
        """
        List of n random floats that sum exactly to 1.0.

        Args:
            n ([type]): Length of list to be returned

        Returns:
            List[float]: A list of floats that sum to 1.0, e.g. [0.2, 0.65, 0.15]
        """
        random_props = [random.random() for _ in range(n-1)]
        random_sum = sum(random_props)
        random_props = [round((random_props[i]/random_sum), 2) for i in range(len(random_props))]
        random_props.append(1.0 - sum(random_props))
        return random_props
    
    def _transfer_discrete(self, receiver: str, amt: float) -> None:
        """
        Transfers amount from house_address to receiver in random discrete amounts, intervals.

        Args:
            receiver (str): Receiver's deposit address.
            amt (float): Amount to be transferred.
        """        
        num_addresses_receiver = self.deposit_addresses_to_wallet[receiver].get_num_addresses()
        n_random_proportions = self._get_n_random_proportions(num_addresses_receiver)

        # Random sleep time between 0 to 2.5 seconds
        random_sleep_times = [random.uniform(0, 2.5) for _ in range(num_addresses_receiver-1)]
        self._transfer_amount(self._house_address, receiver, n_random_proportions[0] * amt, is_minted=False)

        for i in range(1, len(n_random_proportions)):
            time.sleep(random_sleep_times[i-1])
            self._transfer_amount(self._house_address, receiver, n_random_proportions[i] * amt, is_minted=False)


    def contains_key(self, address: str) -> bool:
        """
        If deposit address exists in JobcoinMixer.

        Args:
            address (str): Deposit address.

        Returns:
            bool: True if exists. False otherwise.
        """        
        return address in self.deposit_addresses_to_wallet

    def get_transactions(self, address: str) -> str:
        """
        Returns a list of transactions associated with a given deposit address.
        If address is None, get all transactions in JobcoinMixer.

        Args:
            address ([type], optional): Deposit address associated with a wallet. Could be None.

        Returns:
            str: A balance and list of transactions associated with address as JSON string. If address is None, get all transactions from mixer.
        """            
        if address == None:
            return str([xact.return_transaction() for xact in self.transaction_queue])

        elif address not in self.deposit_addresses_to_wallet:
            return str([])
        
        else:
            return self.deposit_addresses_to_wallet[address].get_transaction_history()

    def get_fees_collected(self) -> float:
        """
        Get all fees collected by JobcoinMixer.

        Returns:
            float: Fees collected from all transactions so far.
        """        
        return self.fees_collected


class APIBasedMixer:
    API_ENV_URL = "http://jobcoin.gemini.com/iodine-defrost"

    """
    A class that simulates the JobcoinMixer.
    """
    def __init__(self, fee_percentage: float = 0.02):
        """
        Initialize the mixer with a fee percentage

        Args:
            fee_percentage (float, optional): Percentage fee to charge per transaction. Defaults to 0.02.
        """                
        self.deposit_addresses = set()
        self._house_address = "house_" + uuid.uuid4().hex
        self.fee_percentage = fee_percentage
        self.fees_collected = 0.0
    
    def get_deposit_address(self, private_addresses: List[str]) -> str:
        """
        Get a fresh deposit address from Mixer.

        Args:
            deposit_addresses (List[str]): A list of private addresses.

        Returns:
            str: A unique deposit address associated with user's wallet
        """        
        new_address = uuid.uuid4().hex

        while new_address in self.deposit_addresses:
            new_address = uuid.uuid4().hex
        
        self.deposit_addresses.add(new_address)
        return new_address
    
    def execute_transaction(self, sender: str, receiver: str, amount: str, is_minted) -> Optional[str]:
        """
        Execute a transaction through the JobcoinMixer.

        Args:
            transaction (Transaction): A valid transaction initiated.
            is_minted (bool, optional): Whether the transaction involvde the coins minted i.e. no sender. Defaults to False.
        """        
        fee = float(amount) * self.fee_percentage
        amount_after_fee = float(amount) - fee
        print("Transaction fee is", fee)
        print("Amt after fee is", amount_after_fee)

        # We also charge the fee for minted transactions
        response = self._transfer_amount(sender, self._house_address, amount, is_minted)
        if response.status_code != requests.codes.ok:
            return response.text

        self._transfer_discrete(receiver, amount_after_fee)
        self.fees_collected += fee

    def _transfer_amount(self, sender: str, receiver: str, amt: str, is_minted: bool):
        """
        Transfers an amount from sender to receiver directly. Sender could be house_address.
        If is_minted, receiver receives balance from network.

        Args:
            sender (str): Sender's deposit address. Could be '(new)' if is_minted.
            receiver (str): Receiver's deposit address.
            amt (str): Amount.
            is_minted (bool): If coins were minted from network.
        """
        print("Transferring {} from {} to {}, is_minted: {}".format(amt, sender, receiver, is_minted))        
        if is_minted:
            # Run /create call to receiver, sender doesn't matter
            payload = {"address": receiver}
            r = requests.post("{}/create".format(APIBasedMixer.API_ENV_URL), data=payload)
        else:
            # Run /post call
            payload = {"fromAddress": sender, "toAddress": receiver, "amount": amt}
            r = requests.post("{}/api/transactions".format(APIBasedMixer.API_ENV_URL), data=payload)

        return r


    def _get_n_random_proportions(self, n) -> List[float]:
        """
        List of n random floats that sum exactly to 1.0.

        Args:
            n ([type]): Length of list to be returned

        Returns:
            List[float]: A list of floats that sum to 1.0, e.g. [0.2, 0.65, 0.15]
        """
        random_props = [random.random() for _ in range(n-1)]
        random_sum = sum(random_props)
        random_props = [round((random_props[i]/random_sum), 2) for i in range(len(random_props))]
        random_props.append(1.0 - sum(random_props))
        return random_props
    
    def _transfer_discrete(self, receiver: str, amt: float) -> None:
        """
        Transfers amount from house_address to receiver in random discrete amounts, intervals.

        Args:
            receiver (str): Receiver's deposit address.
            amt (float): Amount to be transferred.
        """        
        num_batches = random.randint(2, 6)
        n_random_proportions = self._get_n_random_proportions(num_batches)

        # Random sleep time between 0 to 2.5 seconds
        random_sleep_times = [random.uniform(0, 2.5) for _ in range(num_batches-1)]
        self._transfer_amount(self._house_address, receiver, str(n_random_proportions[0] * amt), is_minted=False)

        for i in range(1, len(n_random_proportions)):
            time.sleep(random_sleep_times[i-1])
            self._transfer_amount(self._house_address, receiver, str(n_random_proportions[i] * amt), is_minted=False)


    def get_transactions(self, address: str) -> str:
        """
        Returns a list of transactions associated with a given deposit address.
        If address is None, get all transactions in JobcoinMixer.

        Args:
            address ([type], optional): Deposit address associated with a wallet. Could be None.

        Returns:
            str: A balance and list of transactions associated with address as JSON string. If address is None, get all transactions from mixer.
        """            
        if address == None:
            r = requests.get("{}/api/transactions".format(APIBasedMixer.API_ENV_URL))
        else:
            r = requests.get("{}/api/addresses/{}".format(APIBasedMixer.API_ENV_URL, address))

        return r.json()

    def get_fees_collected(self) -> float:
        """
        Get all fees collected by JobcoinMixer.

        Returns:
            float: Fees collected from all transactions so far.
        """        
        return self.fees_collected