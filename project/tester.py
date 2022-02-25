import requests

url = "http://jobcoin.gemini.com/iodine-defrost/api"

# Get address balance
print("Get address balance!")

address = "Rishab"
r = requests.get("{}/addresses/{}".format(url, address))
print(r.status_code)
print(r.text)
print(r.content)
print(r.json())


# Get all transactions
print("Get all Xacts!")
r = requests.get("{}/transactions".format(url))
print(r.status_code)
print(r.text)
print(r.content)
print(r.json())

# Mint coins
print("Mint 50 coins!")
payload = {"address": "Bob"}
r = requests.post("https://jobcoin.gemini.com/iodine-defrost/create", data=payload)
print(r.status_code)
#print(r.content)

# Send without failure
print("Send money without failure!")
payload = {"fromAddress": "Rishab", "toAddress": "sehaj", "amount": "10"}
r = requests.post("{}/transactions".format(url), data=payload)
print(r.status_code)

# Send to a new address
print("Send money to a new address!")
payload = {"fromAddress": "Rishab", "toAddress": "John", "amount": "10"}
r = requests.post("{}/transactions".format(url), data=payload)
print(r.status_code)
print(r.text)

# Send with failure
print("Send money with failure!")
payload = {"fromAddress": "Rishab", "toAddress": "sehaj", "amount": "100"}
r = requests.post("{}/transactions".format(url), data=payload)
#r.raise_for_status()
print(r.status_code)
print(r.text)
