# Jobcoin Mixer

[![btc-mixer](https://circleci.com/gh/rishab231/btc-mixer.svg?style=shield)](https://app.circleci.com/pipelines/github/rishab231/btc-mixer)

## Quickstart guide
```sh
git clone https://github.com/rishab231/btc-mixer.git
cd btc-mixer
```

**To run tests:**
```zsh
pip install pyenv # Install pyenv if not already installed
pyenv install 3.6.5 # Install Python 3.6.5 for our project
pyenv virtualenv 3.6.5 rishab # Creates a new virtualenv named 'rishab'
pyenv activate rishab # Activate virtualenv 'rishab'
pipenv install -r requirements.txt # Install requirements for project
pipenv run pytest # Run tests
```

**To interact with the application via cli:**
```zsh
# From /btc-mixer run
python -m project.cli
>>>
Welcome to the Jobcoin network!
Please enter your command
[blank to quit] > help # Type 'help' inside tool to see list of supported commands
```

## What is a coin mixer?
Jobcoin is a cryptocurrency; you can think of it as similar to Bitcoin but easier to work with. One of the key features of a digital currency is its decentralized and anonymous nature -- transactions from your account cannot be traced back to reveal your identity. 

A coin mixer is one way to maintain your privacy on a decentralized network. In order to not tie certain addresses to individuals by retracing publicly available transactions, a coin mixer intends to obscure the transactions associated with an address, here is the intended flow for a coin mixer:
1. You provide a list of new, unused addresses that you own to the mixer;
2. The mixer provides you with a new deposit address that it owns;
3. You transfer your bitcoins to that address;
4. The mixer will detect your transfer by watching or polling the P2P Bitcoin network;
5. The mixer will transfer your bitcoin from the deposit address into a big “house account” along with all the other bitcoin currently being mixed; and
6. Then, over some time the mixer will use the house account to dole out your bitcoin in smaller discrete increments to the withdrawal addresses that you provided, possibly after deducting a fee.


## Architecture diagram:
![Architecture diagram](https://github.com/rishab231/btc-mixer/blob/master/architecture_diagram.png)

### Implementation details:
This design uses an object-oriented approach, with natural extensions for scalability, fault-tolerance, and security.

**Jobcoin Network:**
This is the user- or internet-facing entity of our design, which is responsible for the GET (`get_transactions`) and POST operations (`add_addresses`, `send`). Similar to other blockchain networks, the network also mints coins. The logic for minting could be extended based on the mining mechanism of the network.

In this implementation, the user interacts with the network through the command line interface. As shown in the architecture diagram above, interacting with the internet could be easily configured by adding an API layer that converts the HTTP requests to API calls pinging the network.

A network is composed of multiple Jobcoin mixers. The network  acts as a natural load balancer for sharding users and requests across these mixers; this could be based on geographical region of address creation or hash value of address, which we assume will be uniformly distributed due to the random nature of address creation.

**Jobcoin Mixer:**
In terms of architecture, you can think of each mixer hosted independently in an availability zone with multiple database replicas for fault-tolerance. An address on one mixer can interact with addresses on other mixers through the network.

The mixer handles most of the backend logic of the coin mixing. A mixer has a `house_address` where the coins are mixed and held, somewhat similar to an escrow account. It also has an associated `fee_percentage`. A request to add a list of addresses is served by the mixer by creating a new unique `deposit_address` for the user and an associated `Wallet`. A mixer holds multiple such user wallets. *Valid* transactions are executed by the mixer (see `execute_transaction`) once verified by the network. The mixer transfers the entire amount from the sender's `deposit_address` to the `house_address`, from where, after deducting a fee, they are transferred to the receiver's `deposit_address` in discrete amounts and time intervals.

An invariant of this is that the `house_balance` once pending transactions have cleared represents the fees collected by the mixer. These transactions are stored in a `transaction_queue` for easy access on a `get_transactions` call.

**Wallet:**
A wallet is owned by a user, and has attributes `private_addresses`, a list of private addresses, a unique `deposit_address`, current account `balance`, and a list `transactions` executed by the wallet. The entity supports `increase_balance`, `decrease_balance`, and returning a human readable summary of the account via `get_transaction_history`.

**Transaction:**
This class captures a transaction on the JobCoinNetwork, and has attributes `fromAddress`, `toAddress`, `amount`, and `timestamp`. Transaction validity has already been verified by network. A Transaction supports basic `get` methods for attributes, and returnign a human readable summary of the transaction via `return_transaction`.


### Salient features of project:
- Network uses data and method abstraction to hide implementation details of Mixer
- Transaction and Wallet entities exemplify encapsulation by storing user data in a single place (single source-of-truth), and interacting with the mixer through public methods
- Type annotations added in code for easier readability and self-documentation
- Both CLI and Jobcoin classes have been tested extensively with 14 tests (Pytest)
- CI/CD pipeline integrated with project (CircleCI)
- Repository documented using Google Python Style Guide
- Custom exceptions such as InsufficientBalanceException and DepositAddressDoesntExistException prevent duplication of code, and promote human-readable error handling

## Future extensions:
1. Add API Layer to serve HTTP requests to/from Jobcoin network
2. Add listener to network to auto-detect transactions that use network's `deposit_address`
3. Add coin-minting logic based on network's mining protocol
4. Composite multiple mixers for the network and partition users and requests based on `hash(deposit_address)`
5. Each mixer can have associated NoSQL databases with replicas (leader/follow pattern)
    - **Why NoSQL?**
    - Cryptocurrency network, by design, has a data-intensive workload
    - Event-driven architecture more suited for NoSQL DB
    - Easier scalability across multiple replicas
    - Wallet and transactions are semi-structured in nature
    - Frequently used "hot" accounts are easier to cache
    - Data encapsulation ensures we don't have relationships between data, thus preventing need for expensive joins
6. Add cache between Mixer and DB to store high-volume and frequent users such as insitutional clients and power individuals such as traders
7. Instead of suspending thread execution using `time.sleep`, execute discrete transactions asynchronously and return a `Future`
