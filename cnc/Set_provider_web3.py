var Web3 = require('web3');

var web3 = new Web3(new Web3.providers.HttpProvider('https://mainnet.infura.io/v3/81e9fa94b36c42aea3670592b1eae46c'));

web3.eth.net.isListening()
.then(() => console.log('Connected to Ethereum network'))
.catch(e => console.log('Wow. Something went wrong'));

