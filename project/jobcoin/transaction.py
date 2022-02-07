from datetime import datetime, timezone

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
        return self.amount

    def return_transaction(self):
        return str(dict(zip(["timestamp", "fromAddress", "toAddress", "amount"], [self.timestamp, self.fromAddress, self.toAddress, self.amount])))