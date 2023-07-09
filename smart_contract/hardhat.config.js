require('@nomiclabs/hardhat-waffle');

module.exports = {
  solidity: '0.8.0',
  networks: {
    sepolia: {
      url: 'https://eth-sepolia.g.alchemy.com/v2/bh1uuxRsPU9u_zz_srREoZXXcPBfnrkh',
      accounts: ['a75497d8a3d7ad83cc31d5f6afd7807befd5b401a0aa649ccdcca7f8f151353a'],
    },
  },
};