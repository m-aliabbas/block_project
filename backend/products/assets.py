import uuid
from backend.config import STARTING_BALANCE
# STARTING_BALANCE=1000

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
# from backend.blockchain.blockchain import BlockChain
from cryptography.hazmat.primitives.asymmetric.utils import (encode_dss_signature,decode_dss_signature)
import json
from cryptography.exceptions import InvalidSignature
from products.models import Products
from django.contrib.auth.models import User
class Assets:
    def __init__(self,blockchain=None,address=''):
        self.blockchain=blockchain
        # self.address=str(uuid.uuid4())[0:8]
        self.address=address
        self.private_key=ec.generate_private_key(ec.SECP256K1(),default_backend())
        self.public_key=self.private_key.public_key()
        self.serialize_public_key()
    def set_address(self,address):
        self.address=address
    @property
    def products(self):
        return Assets.createProducts(self.blockchain,self.address)
    def sign(self,data):
        """
        It will generate the signature for data on local private key
        """
        return decode_dss_signature(self.private_key.sign(json.dumps(data).encode('utf-8'),ec.ECDSA(hashes.SHA256())))
    def serialize_public_key(self):
        """
        Reset the public key to its serialized version.
        """
        self.public_key = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
    @staticmethod
    def verify(public_key, data, signature):
        """
        Verify a signature based on the original public key and data.
        """
        deserialized_public_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )

        (r, s) = signature

        try:
            deserialized_public_key.verify(
                encode_dss_signature(r, s),
                json.dumps(data).encode('utf-8'),
                ec.ECDSA(hashes.SHA256())    
            )
            return True
        except InvalidSignature:
            return False
    @staticmethod
    def createProducts(blockchain,address):
        """
        Calculate the ba;ance of given address considering transaction data within the blockchain.

        """
        if address=="":
            id=0
        else:
            user=User.objects.get(username=address)
            id=user.id

        try:
            data = Products.objects.all().filter(ToBeSell=True,p_owner=id)
            products=list(data.values_list('id', flat=True))
        except Exception as e:
            raise Exception(f'Some database issue {e}')
        if not blockchain:
            return products
        try:
            for block in blockchain.chain:
                for transaction in block.data:
                    if transaction['input']['address']==address:
                        products=transaction['output'][address]
                    elif address in transaction['output']:
                        products+=[transaction['output'][address]]
        except:
            pass
        return products



    