const Web3 = require('web3');
const axios = require('axios');
const Moralis = require('moralis');
const readline = require('readline');
const fs = require('fs');

const web3 = new Web3();

async function getBalance(privateKey) {
    const account = web3.eth.accounts.privateKeyToAccount(privateKey);
    const balanceWei = await web3.eth.getBalance(account.address);
    const balance = web3.utils.fromWei(balanceWei, 'ether');
    console.log(`Address: ${account.address}, Balance: ${balance} ETH`);
}

async function getPrice() {
    const response = await axios.get('https://deep-index.moralis.io/api/v2/price/ethusd', {
        headers: {
            'X-API-Key': 'YOUR_MORALIS_API_KEY',
        },
    });
    return response.data.price;
}

async function getERC20TokenBalance(privateKey) {
    const account = web3.eth.accounts.privateKeyToAccount(privateKey);
    try {
        await Moralis.start({
            apiKey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjU1MWFiYjdjLTQ4MWItNDQ0My1hYmY0LWQyMjdiYmRmYmZlYSIsIm9yZ0lkIjoiMzQ4OTM3IiwidXNlcklkIjoiMzU4NjYwIiwidHlwZUlkIjoiNzEzNjg5MzItMGMyYy00MWIwLWI4OWItOTExNDY1ZGMzYjRhIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE2ODk3MzM0MjgsImV4cCI6NDg0NTQ5MzQyOH0.de8Yc23bW3Tsi-7sIXzpwUBwlCzM_ykgMm64KPwk5Oc"
        });

        const response = await Moralis.EvmApi.token.getWalletTokenBalances({
            "chain": "0x1",
            "address": account.address
        });

        console.log(response.raw);
    } catch (e) {
        console.error(e);
    }
}

async function main() {
    const fileStream = fs.createReadStream('keys.txt');

    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    for await (const line of rl) {
        const privateKey = line;
        await getBalance(privateKey);
        const price = await getPrice();
        console.log(`The current price of Ethereum is $${price}`);
        await getERC20TokenBalance(privateKey);
    }
}

main().catch(console.error);
