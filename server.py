import grpc 
import numstore_pb2
import numstore_pb2_grpc
import math
import random
from concurrent import futures
import threading

lock = threading.Lock() #protects global vars 

server_dict={}
count=0
cache={}

class Server_imp(numstore_pb2_grpc.NumStoreServicer):
    def SetNum(self, sn1,sn2):
        print(f"setnum {sn1.key}: {sn1.value}")
        lock.acquire()
        global count
        if sn1.key in server_dict.keys():
            oldval = server_dict.get(sn1.key)
            count -= oldval
            
        count+=sn1.value
        server_dict[sn1.key]=sn1.value
        total = count
        lock.release()
        print(f"total: {total}")
        return numstore_pb2.SetNumResponse(total = total)
    
    def Fact(self, f1,f2):
        print(f"fact: {f1.key}")
        lock.acquire() #protect server_dict and cache
        value = server_dict.get(f1.key)
        global cache
        if value == None:
            lock.release()
            return numstore_pb2.FactResponse(error="Not Found")
        else:
            if value in cache.keys():
                ret = cache[value]
                lock.release()
                print(f"return value: {ret} hit=True")
                return numstore_pb2.FactResponse(value=ret, hit=True) #tried many things, idk what to put for this line :/
            else: 
                #LRU
                if len(cache)>=10:
                    remove = min(cache, key=cache.get)
                    del cache[remove]
                res = math.factorial(value)
                cache[value] = numstore_pb2.FactResponse(value=res)
                lock.release()
                print(f"return value: {res} hit=False")
                return numstore_pb2.FactResponse(value=res, hit=False)
        
        
        
def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    numstore_pb2_grpc.add_NumStoreServicer_to_server(Server_imp(), server)
    server.add_insecure_port("[::]:5440")
    server.start()
    server.wait_for_termination()
if __name__ == '__main__':
    server()
