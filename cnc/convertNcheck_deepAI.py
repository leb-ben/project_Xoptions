import json
import requests
from web3 import Web3
from eth_account import Account

INFURA_API_KEY = "81e9fa94b36c42aea3670592b1eae46c"

# Infura API endpoints for different networks
INFURA_API_ENDPOINTS = {
    "mainnet": "https://mainnet.infura.io/v3/%s" % INFURA_API_KEY,
    "polygon": "https://polygon-mainnet.infura.io/v3/%s" % INFURA_API_KEY,
    "optimism": "https://optimism-mainnet.infura.io/v3/%s" % INFURA_API_KEY,
    "arbitrum": "https://arbitrum-mainnet.infura.io/v3/%s" % INFURA_API_KEY,
    "palm": "https://palm-mainnet.infura.io/v3/%s" % INFURA_API_KEY,
    "avalanche": "https://avalanche-mainnet.infura.io/v3/%s" % INFURA_API_KEY,
    "near": "https://near-mainnet.infura.io/v3/%s" % INFURA_API_KEY,
    "aurora": "https://aurora-mainnet.infura.io/v3/%s" % INFURA_API_KEY,
    "starknet": "https://starknet-mainnet.infura.io/v3/%s" % INFURA_API_KEY,
    "celo": "https://celo-mainnet.infura.io/v3/%s" % INFURA_API_KEY
}

# Kraken API endpoint and asset pair
KRAKEN_API_ENDPOINT = "https://api.kraken.com/0/public/Ticker"
ASSET_PAIR = "ETHUSD"

# NFT API endpoint
NFT_API_ENDPOINT = "https://nft.api.infura.io/ethereum/mainnet"

# Initialize total balance variables
total_balance_ether = 0
total_balance_usd = 0

# Initialize Web3 instances for each network
web3_instances = {}
for network, endpoint in INFURA_API_ENDPOINTS.items():
    web3_instances[network] = Web3(Web3.HTTPProvider(endpoint))

# Read keys from keys.txt file
with open("keys.txt") as f:
    for line in f:
        # Remove newline character at the end of the line
        priv_key = line.strip()
        if len(priv_key) != 66 or not priv_key.lower().startswith("0x"):
            raise ValueError("Invalid private key format: %s" % priv_key)
        # Create account from private key
        acct = Account.from_key(priv_key)
        # Get address from account
        address = acct.address
        # Print address
        print("Address: %s" % address)
        
        # Initialize balances dictionary for the wallet
        balances = {"ETH": 0}
        
        # Query ETH balance for the address using the Ethereum network Web3 instance
        balance_wei = web3_instances["mainnet"].eth.get_balance(address)
        # Convert balance to Ether units
        balance_ether = balance_wei / 1000000000000000000  # 1 Ethereum = 10^18 Wei
        # Print balance
        print("Balance (ETH): %.5f Ether" % balance_ether)
        
        # Update total balance
        total_balance_ether += balance_ether
        balances["ETH"] += balance_ether
        
        # Get current Ether price in USD from Kraken API
        response = requests.get(KRAKEN_API_ENDPOINT, params={"pair": ASSET_PAIR})
        if response.ok:
            result = response.json().get("result")
            if result and isinstance(result, dict):
                last_trade_price = float(result.get(ASSET_PAIR).get("c")[0])
            else:
                raise ValueError("Invalid Kraken API response: %s" % response.content)
        else:
            raise ValueError("Kraken API error: %s" % response.status_code)
        
        # Convert Ether balance to USD
        balance_usd = balance_ether * last_trade_price
        # Update total balance
        total_balance_usd += balance_usd
        
        # Print USD balance
        print("Balance (USD): $%.2f" % balance_usd)
        
        # Query token balances for the address on each network using the respective Web3 instances
        for network, web3_instance in web3_instances.items():
            if network == "mainnet":
                continue  # Skip Ethereum network since we already retrieved the ETH balance
            
            # Define token contract addresses and decimals for each network
            if network == "polygon":
                contract_address = "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"  # USDC contract address
            elif network == "optimism":
                contract_address = "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1"  # USDC contract address on Optimism
            # Add more contract addresses and decimals for other networks here
            
            # Create ERC20 contract instance for the token on the network
            contract_instance = web3_instance.eth.contract(address=contract_address, abi=ERC20_ABI)
            # Query token balance for the address using the contract instance
            token_balance_wei = contract_instance.functions.balanceOf(address).call()
            # Convert token balance to token units (USDC is a 6-decimal token)
            decimals = 6 if network in ["polygon", "optimism"] else contract_instance.functions.decimals().call()
            token_balance = token_balance_wei / 10 ** decimals
            # Update balances dictionary for the token
            token_symbol = contract_instance.functions.symbol().call()
            balances[token_symbol] = token_balance
            
        # Print balances for all networks and tokens
        print("Balances: %s" % json.dumps(balances, indent=4))
        
        # Query NFTs held by the address using the NFT API endpoint
        response = requests.get(NFT_API_ENDPOINT, params={"owner": address})
        if response.ok:
            result = response.json().get("result")
            if result and isinstance(result, list):
                num_nfts = len(result)
                print("Number of NFTs owned: %d" % num_nfts)
            else:
                raise ValueError("Invalid NFT API response: %s" % response.content)
        else:
            raise ValueError("NFT API error: %s" % response.status_code)
        
        print("")  # Print empty line for readability

# Print grand total balance
print("Grand Total Balance: %.5f Ether = $%.2f USD" % (total_balance_ether, total_balance_usd))

# ERC20 ABI for querying token balances
ERC20_ABI = [
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
]