from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from cryptography.fernet import Fernet
import random
import socket

key = Fernet.generate_key()
fernet = Fernet(key)

class messenger(DatagramProtocol):
    def __init__(self, host, port):
        if host == "localhost":
            host = "127.0.0.1"
        self.id = host, port
        print("Running on: ", self.id)
        print("User Key: ",key.decode())
        self.address = input("Write address: "), int(input("Write port: "))
        c_key = input("Enter Client Key: ").encode()
        global c_fernet
        c_fernet = Fernet(c_key)
        reactor.callInThread(self.send_message)
    
    def datagramReceived(self, datagram, addr):
        print(addr," : ",c_fernet.decrypt(datagram).decode())
    
    def send_message(self):
        while True:
            txt = input(":::")
            if(txt == "$exit"):
                reactor.stop()
                break
            else:
                entxt = fernet.encrypt(txt.encode())
                self.transport.write(entxt, self.address)

if __name__ == '__main__':
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    port = random.randint(1000,5000)
    while a_socket.connect_ex((local_ip,port)) == 0:
        port = random.randint(1000,5000)
        a_socket.close()
    a_socket.close()
    reactor.listenUDP(port, messenger(local_ip, port))
    reactor.run()