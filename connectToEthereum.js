const Web3 = require('web3');
const axios = require('axios');
const fs = require('fs');
require('dotenv').config();

// Load your Infura key from the .env file
const infuraKey = process.env.81e9fa94b36c42aea3670592b1eae46c;
const web3 = new Web3(new Web3.providers.HttpProvider(`https://mainnet.infura.io/v3/${infuraKey}`));

async function checkBalance(privateKey) {
    const account = web3.eth.accounts.privateKeyToAccount(privateKey);
    const balance = await web3.eth.getBalance(account.address);
    return { address: account.address, balance: web3.utils.fromWei(balance, 'ether') };
}

async function getPrice() {
    const response = await axios.get('https://api.priceapi.com');  // Replace with real API
    return response.data.price;  // Replace with real key
}

function readKeysFromFile() {
    const data = fs.readFileSync('keys.txt', 'utf-8');
    return data.split('\n');
}

async function checkAllBalances() {
    const keys = readKeysFromFile();
    let totalBalance = 0;
    for (const key of keys) {
        const { address, balance } = await checkBalance(key);
        console.log(`Address: ${address}, Balance: ${balance} ETH`);
        totalBalance += parseFloat(balance);
    }
    const price = await getPrice();
    console.log(`Total balance: ${totalBalance} ETH, ~$${totalBalance * price}`);
}

checkAllBalances();
