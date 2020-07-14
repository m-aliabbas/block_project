from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block
from backend.blockchain.blockchain import BlockChain
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.products.assets_transact import AssetsTransaction
from backend.products.assets_transpool import AssetsTransPool
pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-ad524a58-b6ec-11ea-875a-ceb74ea8e96a'
pnconfig.publish_key = 'pub-c-d5bf2ec2-6d97-49d3-88ed-9fd655e4aac6'

blockchain=BlockChain()
TEST_CHANNEL='TEST_CHANNEL'
BLOCK_CHANNEL='BLOCK_CHANNEL'
CHANNELS={
    'TEST':'TEST',
    'BLOCK':'BLOCK',
    'TRANSACTION':'TRANSACTION',
    'ASSETS':'ASSETS'
}



class Listener(SubscribeCallback):
    def __init__(self,blockchain,transaction_pool,assetPool):
        self.blockchain=blockchain
        self.transaction_pool=transaction_pool
        self.assetPool=assetPool
    def message(self,pubnub,message_object):
        print(f'\n Incoming Message : {message_object}')
        if message_object.channel==CHANNELS['BLOCK']:
            block=Block.from_json(message_object.message)
            print('Block to mine ',block)
            potential_chain=self.blockchain.chain
            # potential_chain.append(block)
            print(potential_chain)
            try:
                self.blockchain.replace_chain(potential_chain)
                self.transaction_pool.clear_blockchain_transactions(
                    self.blockchain)
                print('Chain Replaced')
            except Exception as e:
                print(f'Did not replace" {e}')
        elif message_object.channel==CHANNELS['TRANSACTION']:
            transaction=Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print('New Transaction in Pool')
        elif message_object.channel==CHANNELS['ASSETS']:
            assetsTran=AssetsTransaction.from_json(message_object.message)
            self.assetPool.set_transaction(assetsTran)
            print('New Assets Transaction is added')
class PubSub():
    def __init__(self,blockchain,transaction_pool,assetPool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain,transaction_pool,assetPool))
    def publish(self,channel,message):
        self.pubnub.publish().channel(channel).message(message).sync()
    def broadcast_block(self,block):
        self.publish(CHANNELS['BLOCK'],block.to_json())
    def broadcast_transaction(self,transaction):
        """
        This will broadcast transaction
        """
        self.publish(CHANNELS['TRANSACTION'],transaction.to_json())
    def broadcast_asset(self,assetsTran):
        self.publish(CHANNELS['ASSETS'],assetsTran.to_json())