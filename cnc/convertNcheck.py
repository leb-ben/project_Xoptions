import requests
from eth_account import Account
from web3 import Web3

def main():
    # Shared API key for all chains
    api_key = 'e1b71855fcd5414ead187648026de59c'

    # Read the private keys from the keys.txt file
    with open('keys.txt', 'r') as file:
        private_keys = file.read().splitlines()

    # Chain URLs for different networks
    ethereum_url = f'https://mainnet.infura.io/v3/e1b71855fcd5414ead187648026de59c'
    polygon_url = f'https://polygon-mainnet.infura.io/v3/{api_key}'
    optimism_url = f'https://optimism-mainnet.infura.io/v3/{api_key}'
    arbitrum_url = f'https://arbitrum-mainnet.infura.io/v3/{api_key}'
    palm_url = f'https://palm-mainnet.infura.io/v3/{api_key}'
    avalanche_url = f'https://avalanche-mainnet.infura.io/v3/{api_key}'
    near_url = f'https://near-mainnet.infura.io/v3/{api_key}'
    aurora_url = f'https://aurora-mainnet.infura.io/v3/{api_key}'
    starknet_url = f'https://starknet-mainnet.infura.io/v3/{api_key}'
    celo_url = f'https://celo-mainnet.infura.io/v3/{api_key}'

    # Loop through the private keys and extract the account address
    for private_key in private_keys:
        try:
            account = Account.from_key(private_key)
            address = account.address
            print(f'Public Key: {address}')

            # Check the Ethereum balance
            ethereum_balance = get_balance(ethereum_url, address)
            print(f'Ethereum Balance: {ethereum_balance} ETH')

            # Check the balance on other chains
            polygon_balance = get_balance(polygon_url, address)
            # Add code to check balance for other chains using respective URLs

        except ValueError as e:
            print(f'Error: {str(e)}')

def get_balance(ethereum_url, address):
    try:
        response = requests.get(f'{ethereum_url}/address/{address}/balance')
        if response.status_code == 200:
            balance = response.json().get('balance', 0)
            return balance
        else:
            print(f'Error: {response.status_code} - {response.text}')
            return 0
    except requests.exceptions.RequestException as e:
        print(f'Request error: {e}')
        return 0

if __name__ == '__main__':
    main()
