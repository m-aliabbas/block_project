import hashlib
import json
def stringify(data):
    return json.dumps(data)
def crypto_hash(*args):
    """
    It will return hash of arguments
    """
    stringified_args=map(stringify,args)
    joined_data=''.join(stringified_args)
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

