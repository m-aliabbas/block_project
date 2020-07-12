from backend.products.assets import Assets
from backend.blockchain.blockchain import BlockChain

blockchain=BlockChain()
assets=Assets(blockchain=blockchain)
product_id=2
recipient='12'
assetTran=AssetsTransaction(sender_wallet=assets,recipient=recipient,product_id=product_id)
