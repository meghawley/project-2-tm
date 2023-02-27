import grpc 
import numstore_pb2
import numstore_pb2_grpc
import math
from concurrent import futures

server_dict={}
count=0

class Server_imp(numstore_pb2_grpc.NumStoreServicer):
    def SetNum(self, sn1,sn2):
        global count
        try:
            oldval = server_dict.get(sn1.key)
            count -= oldval
        except: 
            pass
        count+=sn1.value
        server_dict[sn1.key]=sn1.value
        return numstore_pb2.SetNumResponse(total = count)
    
    def Fact(self, f1,f2):
        value = server_dict.get(f1.key)
        if value == None:
            return numstore_pb2.FactResponse(error="Not Found")
        else:
            return numstore_pb2.FactResponse(value = math.factorial(value))
def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    numstore_pb2_grpc.add_NumStoreServicer_to_server(Server_imp(), server)
    server.add_insecure_port("[::]:5440")
    server.start()
    server.wait_for_termination()
if __name__ == '__main__':
    server()