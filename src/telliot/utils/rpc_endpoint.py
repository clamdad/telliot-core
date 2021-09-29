"""
Utils for:
- creating a JSON RPC connection to an EVM blockchain
- connecting to an EVM contract
"""
from enum import Enum
from typing import AnyStr
from typing import Optional

import web3
from pydantic.dataclasses import dataclass
from pydantic.main import BaseModel
from web3 import Web3


class RPCEndpoint(BaseModel):
    """JSON RPC Endpoint for EVM compatible network"""

    #: Blockchain Name
    # chain = Enum(*supported_networks)

    #: Network Name (e.g. 'mainnet', 'testnet', 'rinkebey')
    network: AnyStr

    #: Provider Name (e.g. 'Infura')
    provider: AnyStr

    #: URL (e.g. 'https://mainnet.infura.io/v3/<project_id>')
    url: AnyStr

    #: Web3 Connection
    web3: Optional[Web3]

    class Config:
        arbitrary_types_allowed = True

    def connect(self):
        """Connect to EVM blockchain"""
        self.web3 = Web3(Web3.HTTPProvider(self.url))
        try:
            connected = self.web3.isConnected()
        # Pokt nodes won't submit isConnected rpc call
        except Exception as e:
            connected = self.web3.eth.get_block_number() > 1
        if connected:
            print("Connected to {}".format(self))
        else:
            print("Could not connect to {}".format(self))

        return self.web3

    def close(self):
        self.web3 = None


@dataclass
class Contract:
    """Convenience wrapper for connecting to an Ethereum contract"""

    #: RPCNode connection to Ethereum network
    node: RPCEndpoint

    address: str

    #: Abi specifications of contract, likely loaded from JSON
    abi: str

    def connect(self):
        """Connect to EVM contract through an RPC Endpoint"""
        self.Contract = self.node.web3.eth.contract(address=self.address, abi=self.abi)
