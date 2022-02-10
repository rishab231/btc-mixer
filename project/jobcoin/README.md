## Todo: 
1. [NOTREQD] Abstract away the HTTP requests initially
2. [DONE] Add unit tests for jobcoin.py main functions
3. [NOTREQD] Create JobCoin network that listens in on transactions
4. [NOTREQD] Futures block for async execution of discrete transactions
5. [DONE] Add exceptions for Insufficient balance, malformed JSON
6. [DONE] Get list of global transactions
7. [DONE] Add doc strings to functions -- look at Prob140
8. [DONE] Fix is_minted logic -- right now it's sender == None
9. Add 'info' logging
10. [DONE] Every class into its own file
11. Update README
12. [DONE] Support cmd-c, cmd-d breaks for cli
13. [DONE] Construct requirements.py
14. [DONE] Add more CLI tests
15. [DONE] Amount float vs int
17. [DONE] Typing for return values of functions
19. [DONE] Create architecture diagram of application
18. Time.sleep can be float?
16. Address todos in code

NEXT: 
1. [DONE] Add more CLI tests
2. [DONE] Integration with CircleCI
3. [DONE] Add license file
4. [DONE] Create architecture diagram of application
5. Update README
6. Address todos in code

## Learnings
- Absolute imports are good
- Directory structure in python is important
- Generating random floats is not trivial, requires thought
- Futures block for async execution of discrete transactions, future send should be blocked
- Listener class that listens in on network transactions
- CircleCI build

Run using python -m project.cli

## Improvements
- Scale out multiple mixers for parallelization
- Different mixers in different geographical regions
- Partitioning based on deposit_address
- Each with multiple replicas

- Institutional users can cache requests
NoSQL databases can be used for easier scalability and fewer relationships between datasets
- Hash of addresses can also be used as keys for partitioning since we can assume keys are distributed randomly