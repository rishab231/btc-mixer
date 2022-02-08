from datetime import datetime, timezone

class Transaction:
    """
    Captures a transaction on the JobCoinNetwork. Transaction validity has been verified by network.
    """    
    def __init__(self, fromAddress: str, toAddress: str, amount: str):
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount
        self.timestamp = datetime.now(timezone.utc).isoformat(sep='T')
    
    def get_from_address(self) -> str:
        """
        Gets a transaction's fromAddress.

        Returns:
            str: Deposit address of sender. Could be '(new)' if coins were minted.
        """               
        return self.fromAddress
    
    def get_to_address(self) -> str:
        """
        Gets a transaction's toAddress.

        Returns:
            str: Deposit address of receiver.
        """        
        return self.toAddress
    
    def get_amount(self) -> str:
        """
        Amount associated with transaction.

        Returns:
            str: Amount as string.
        """        
        return self.amount

    def return_transaction(self) -> str:
        """
        Returns a human readable summary of transaction, with associated timestamp, fromAddress, toAddress, and amount.

        Returns:
            str: Summary of transaction
            example: {'timestamp': '2022-02-08T04:59:10.709213+00:00', 'fromAddress': '8b..a9', 'toAddress': 'a3..86', 'amount': '90.0'}
        """        
        return str(dict(zip(["timestamp", "fromAddress", "toAddress", "amount"], [self.timestamp, self.fromAddress, self.toAddress, self.amount])))