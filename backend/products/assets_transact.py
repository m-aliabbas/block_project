import uuid
import time
from backend.products.assets import Assets
from backend.config import MINING_REWARD,MINING_REWARD_INPUT
# from backend.blockchain.blockchain import BlockChain
class AssetsTransaction:
    """
    This class will be responisble for currancy exchange.

    """
    def __init__(self,sender_wallet=None,recipient=None,product_id=None,id=None,output=None,input=None):
        self.id=id or str(uuid.uuid4())[0:8] 
        self.output=output or self.create_output(sender_wallet,recipient,product_id )
        self.input=input or self.create_input(sender_wallet,self.output)
    def create_output(self,sender_wallet,recipient,product_id):
        # if amount>sender_wallet.balance:
        #     raise Exception('Amount Exceeds Balance')
        output={}
        try:
            output[recipient]=[product_id]
            prod=sender_wallet.products
            prod.remove(product_id)
            output[sender_wallet.address]=prod
        except ValueError:
            raise Exception('Product does not exists')
        return output
    def create_input(self,sender_wallet,output):
        """
            This will sign the transection.
            Structure the input data for transaction

        """
        return {
                'timestamp':time.time_ns(),
                'products':sender_wallet.products,
                'address':sender_wallet.address,
                'public_key':sender_wallet.public_key,
                'signature':sender_wallet.sign(output)
            }
    def update(self,sender_wallet,recipient,product_id):
        """
        It will update the transaction with new and old recipent
        """
        if product_id not in self.output[sender_wallet.address]:
            raise Exception('Product does not exists in sender assets')
        

        if recipient in self.output:
            self.output[recipient]=self.output[recipient]+[product_id]
            
        else:
            self.output[recipient]=[product_id]
           
        try:
            prod=self.output[sender_wallet.address]
            prod.remove(product_id)
            self.output[sender_wallet.address]=prod
        except ValueError:
            print('not in list')
        self.input=self.create_input(sender_wallet,self.output)
    def to_json(self):
        return self.__dict__
    @staticmethod
    def from_json(transaction_json):
        """
        It will back
        """
        return AssetsTransaction(**transaction_json)
    @staticmethod
    def is_valid_transaction(transaction):
        """
        Validate a transaction.
        Raise an exception for invalid transactions.
        """
        # if transaction.input == MINING_REWARD_INPUT:
        #     if list(transaction.output.values()) != [MINING_REWARD]:
        #         raise Exception('Invalid mining reward')
        #     return

        # output_total = sum(transaction.output.values())
    
        # if transaction.input['products'] != output_total:
        #     raise Exception('Invalid transaction output values')
        print(transaction.input['products'])
        print(transaction.output)
        if not Assets.verify(
            transaction.input['public_key'],
            transaction.output,
            transaction.input['signature']
        ):
            raise Exception('Invalid signature')




