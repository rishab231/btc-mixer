class InsufficientBalanceException(Exception):
    def __init__(self):
        message = "Insufficient balance in sender's account"
        super().__init__(message)

class DepositAddressDoesntExistException(Exception):
    def __init__(self, address):
        message = "Deposit address ({}) does not exist in the JobMixer".format(address)
        super().__init__(message)