class AssetsTransPool:
    def __init__(self):
        self.transaction_map={}
    def set_transaction(self,transation):
        """
        It set transection in transaction pool
        """

        self.transaction_map[transation.id]=transation
    def existing_transaction(self,address):
        """
        It will look for transcation in Pool.
        """
        for transaction in self.transaction_map.values():
            if transaction.input['address']==address:
                return transaction
        return None
    def transaction_data(self):
        """
        Return transacion in 
        """
        return list(map(lambda transaction: transaction.to_json(),self.transaction_map.values()))
    def clear_blockchain_transactions(self,blockchain):
        """
        Delete blockchain recorded transaction from transaction pools.
        """
        for block in blockchain.chain:
            for transaction in block.data:
                try:
                    del self.transaction_map[transaction['id']]
                except KeyError:
                    pass
        