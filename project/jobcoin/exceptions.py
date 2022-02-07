class InsufficientBalanceException(Exception):
    def __init__(self):
        message = "Insufficient balance in sender's account"
        super().__init__(message)