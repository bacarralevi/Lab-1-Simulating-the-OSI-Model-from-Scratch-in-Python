import socket
import json
import struct
import pickle

# Reduce redundancy
class BaseLayer:
    def send(self, data):
        raise NotImplementedError

    def receive(self, data):
        raise NotImplementedError

class PhysicalLayer(BaseLayer):
    def send(self, data):
        print("[Physical] Sending raw bits...")
        return pickle.dumps(data)  # Serialize data

    def receive(self, data):
        print("[Physical] Receiving raw bits...")
        return pickle.loads(data)  # Deserialize data

class DataLinkLayer(BaseLayer):
    def send(self, data):
        mac_header = {"src": "AA:BB:CC:D1:D2:D3", "dst": "FF:EE:DD:CC:BB:AA"}
        print(f"[Data Link] Framing data with MAC header: {mac_header}")
        return pickle.dumps((mac_header, data))

    def receive(self, data):
        mac_header, payload = pickle.loads(data)
        print(f"[Data Link] Unframing data with MAC header: {mac_header}")
        return payload

class NetworkLayer(BaseLayer):
    def send(self, data):
        ip_header = {"src": "192.168.1.1", "dst": "192.168.1.2"}
        print(f"[Network] Adding IP header: {ip_header}")
        return pickle.dumps((ip_header, data))

    def receive(self, data):
        ip_header, payload = pickle.loads(data)
        print(f"[Network] Stripping IP header: {ip_header}")
        return payload

class TransportLayer(BaseLayer):
    def send(self, data):
        print("[Transport] Adding TCP-like sequencing...")
        seq_number = struct.pack('I', 1001)  # Fixed sequence number
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

# Simulate data transmission
def simulate_osi_model():
    message = input("Enter a message to send: ")
    layers = [
        ApplicationLayer(), PresentationLayer(), SessionLayer(),
        TransportLayer(), NetworkLayer(), DataLinkLayer(), PhysicalLayer()
    ]

    # Sending data
    data = message
    for layer in layers:
        data = layer.send(data)
    
    print("\nTransmitting Data...\n")

    # Receiving data
    for layer in reversed(layers):
        data = layer.receive(data)
    
    print("\nFinal Received Message:", data)


simulate_osi_model()
