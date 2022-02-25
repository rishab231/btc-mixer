## Next steps post Jebril feedback

- Deposit address needs to be created
- Use API calls as backend
- Use decimal over float


## Assumptions
For a given transaction from sender -> receiver at amount:
- sender -> house_address (Starts with `h`) -> deposit_address in discrete intervals
- House_address collects fee, if balance not present (status code) return text
- Discretely send 


## If minted
- Create to house_address
- House address discretely sends coins in batches to the address
- Num batches can be random from 3-6