import grpc 
import numstore_pb2
import numstore_pb2_grpc
import math
import random
from concurrent import futures
import threading
import collections

lock = threading.Lock() #protects global vars 

server_dict={}
count=0
cache=collections.OrderedDict()

class Server_imp(numstore_pb2_grpc.NumStoreServicer):
    def SetNum(self, sn1,sn2):
        #print(f"setnum {sn1.key}: {sn1.value}")
        lock.acquire()
        global count
        if sn1.key in server_dict.keys():
            oldval = server_dict.get(sn1.key)
            count -= oldval
            
        count+=sn1.value
        server_dict[sn1.key]=sn1.value
        total = count
        lock.release()
        #print(f"total: {total}")
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
            #LRU
            print("cache before", cache)
            if value in cache.keys():
                #if its already in the dictionary,
                ret = cache[value]
                del cache[value] #delete the pair
                cache[value] = ret #move the pair to the end of the dictionary
                lock.release()
                print(f"return value: {ret} hit=True")
                print("cache after: ", cache)
                return numstore_pb2.FactResponse(value=int(ret), hit=True) #tried many things, idk what to put for this line :/
            else: 
                #if the cache has no room,
                if len(cache)>=2:
                    #delete the first k-v pair in the dictionary
                    
                    remove = list(cache.items())[0][0] #get key of first entry in dictionary. #min(cache, key=cache.get)
                    print("remove: ", remove)
                    del cache[remove]
                    print("deleted remove")
                res = math.factorial(value)
                cache[value] = res
                lock.release()
                print(f"return value: {res} hit=False")
                print("cache after: ", cache)
                return numstore_pb2.FactResponse(value=int(res), hit=False)
            
        
        
        
def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    numstore_pb2_grpc.add_NumStoreServicer_to_server(Server_imp(), server)
    server.add_insecure_port("[::]:5440")
    server.start()
    server.wait_for_termination()
if __name__ == '__main__':
    server()
