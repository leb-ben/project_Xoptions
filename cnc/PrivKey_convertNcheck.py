import requests
from web3 import Web3

# Define Infura endpoint and API key
infura_endpoint = 'https://mainnet.infura.io/v3/81e9fa94b36c42aea3670592b1eae46c'
web3 = Web3(Web3.HTTPProvider(infura_endpoint))

# Define API endpoint to retrieve current ETH to USD exchange rate from CoinGecko
coingecko_endpoint = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd'

def get_eth_to_usd_rate():
    # Make API request to CoinGecko to retrieve current ETH to USD exchange rate
    response = requests.get(coingecko_endpoint)
    data = response.json()
    # Parse the exchange rate from the response data
    eth_to_usd_rate = data['ethereum']['usd']
    # Return the exchange rate as a float
    return eth_to_usd_rate

def check_balance(private_key):
    # Derive public key from private key
    account = web3.eth.account.from_key(private_key)
    public_key = account.public_key.to_checksum_address()
    # Query the blockchain for balance
    balance = web3.eth.getBalance(public_key)
    # Convert balance from wei to ether
    balance = web3.fromWei(balance, 'ether')
    # Retrieve current ETH to USD exchange rate
    eth_to_usd_rate = get_eth_to_usd_rate()
    # Convert balance to USD
    balance_usd = balance * eth_to_usd_rate
    # Print balance and balance in USD for debugging purposes
    print(f"{public_key}: {balance} ETH ({balance_usd:.2f} USD)")
    # Return balance as string
    return str(balance)

# Read list of private keys from text file
with open("keys.txt", "r") as f:
    private_keys = f.read().splitlines()

# Iterate through list of private keys
for private_key in private_keys:
    # Check balance of private key
    balance = check_balance(private_key)

