import socket
import json
import struct
import pickle

#reduce redundancy
class BaseLayer:
    def send(self, data):
        raise NotImplementedError
    
    def receive(self, data):
        raise NotImplementedError

class PhysicalLayer(BaseLayer):
    def send(self, data):
        print("[Physical] Sending raw bits...")
        return pickle.dumps(data)  #serialize data
    
    def receive(self, data):
        print("[Physical] Receiving raw bits...")
        return pickle.loads(data)  #deserialize data

class DataLinkLayer(BaseLayer):
    def send(self, data):
        print("[Data Link] Framing data...")
        mac_header = {"src": "AA:BB:CC:D1:D2:D3", "dst": "FF:EE:DD:CC:BB:AA"}
        return pickle.dumps((mac_header, data))
    
    def receive(self, data):
        print("[Data Link] Unframing data...")
        _, payload = pickle.loads(data)
        return payload

class NetworkLayer(BaseLayer):
    def send(self, data):
        print("[Network] Adding IP header...")
        ip_header = {"src": "192.168.1.1", "dst": "192.168.1.2"}
        return pickle.dumps((ip_header, data))
    
    def receive(self, data):
        print("[Network] Stripping IP header...")
        _, payload = pickle.loads(data)
        return payload

class TransportLayer(BaseLayer):
    def send(self, data):
        print("[Transport] Adding TCP-like sequencing...")
        seq_number = struct.pack('I', 1001)  #fixed sequence no
        return seq_number + pickle.dumps(data)
    
    def receive(self, data):
        print("[Transport] Processing TCP sequence...")
        return pickle.loads(data[4:])

class SessionLayer(BaseLayer):
    def send(self, data):
        print("[Session] Managing session...")
        return pickle.dumps({"session": "ACTIVE", "data": data})
    
    def receive(self, data):
        print("[Session] Handling session...")
        return pickle.loads(data)["data"]

class PresentationLayer(BaseLayer):
    def send(self, data):
        print("[Presentation] Encoding data...")
        return pickle.dumps(data)
    
    def receive(self, data):
        print("[Presentation] Decoding data...")
        return pickle.loads(data)

class ApplicationLayer(BaseLayer):
    def send(self, data):
        print("[Application] Preparing HTTP-like request...")
        return json.dumps({"request": "GET", "data": data}).encode()
    
    def receive(self, data):
        print("[Application] Parsing HTTP-like request...")
        return json.loads(data.decode())["data"]

#simulate data transmission
def simulate_osi_model():
    message = input("Enter a message to send: ")
    layers = [
        ApplicationLayer(), PresentationLayer(), SessionLayer(),
        TransportLayer(), NetworkLayer(), DataLinkLayer(), PhysicalLayer()
    ]
    
    #sending Data
    data = message
    for layer in layers:
        data = layer.send(data)
    
    print("\nTransmitting Data...\n")
    
    #receiving Data
    for layer in reversed(layers):
        data = layer.receive(data)
    
    print("\nFinal Received Message:", data)


simulate_osi_model()
