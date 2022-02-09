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
19. Create architecture diagram of application
18. Time.sleep can be float?
16. Address todos in code

NEXT: 
1. [DONE] Add more CLI tests
2. Integration with Travis CI
3. Add license file
4. Create architecture diagram of application

## Learnings
Absolute imports are good
Directory structure in python is important
Generating random floats is not trivial, requires thought
Futures block for async execution of discrete transactions
Create JobCoin network that listens in on transactions

Run using python -m project.cli

## Improvements
