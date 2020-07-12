from backend.blockchain.blockchain import BlockChain
import time
from backend.config import SECONDS
blockchain=BlockChain()

times=[]


for i in range(1000):
     start_time=time.time_ns()
     blockchain.addBlock(i)
     end_time=time.time_ns()
     time_to_mine=(end_time-start_time) / SECONDS
     times.append(time_to_mine)
     average_time=sum(times)/len(times)
     print(blockchain.chain[-1])
     print(time_to_mine)
     print(average_time)