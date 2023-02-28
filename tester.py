import sys
import grpc
import numstore_pb2, numstore_pb2_grpc

port = "5440"
addr = f"127.0.0.1:{port}"
channel = grpc.insecure_channel(addr)
stub = numstore_pb2_grpc.NumStoreStub(channel)

# TEST SetNum
resp = stub.SetNum(numstore_pb2.SetNumRequest(key="A", value=1))
print(resp.total) # should be 1
resp = stub.SetNum(numstore_pb2.SetNumRequest(key="B", value=10))
print(resp.total) # should be 11
resp = stub.SetNum(numstore_pb2.SetNumRequest(key="A", value=5))
print(resp.total) # should be 15
resp = stub.SetNum(numstore_pb2.SetNumRequest(key="B", value=0))
print(resp.total) # should be 5
resp = stub.SetNum(numstore_pb2.SetNumRequest(key="C", value=1))
print(resp.total) # should be 5
resp = stub.SetNum(numstore_pb2.SetNumRequest(key="D", value=2))
print(resp.total) # should be 5


# TEST Fact
resp = stub.Fact(numstore_pb2.FactRequest(key="A"))
print(resp.value) # should be 120
resp = stub.Fact(numstore_pb2.FactRequest(key="A"))
print(resp.value) # should be 120
resp = stub.Fact(numstore_pb2.FactRequest(key="B"))
print(resp.value) 
resp = stub.Fact(numstore_pb2.FactRequest(key="C"))
print(resp.value) 
resp = stub.Fact(numstore_pb2.FactRequest(key="D"))
print(resp.value) 
resp = stub.Fact(numstore_pb2.FactRequest(key="C"))
print(resp.value) 
resp = stub.Fact(numstore_pb2.FactRequest(key="A"))
print(resp.value) 
resp = stub.Fact(numstore_pb2.FactRequest(key="B"))
print(resp.value) 