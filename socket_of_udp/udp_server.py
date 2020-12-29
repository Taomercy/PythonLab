import sys
import socket
from time import ctime

HOST = ''
PORT = 8888
BUFSIZ = 1024
ADDRESS = (HOST, PORT)

udpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpServerSocket.settimeout(30.0)
udpServerSocket.bind(ADDRESS)      # 绑定客户端口和地址


def udp_server():
    while True:
        print("waiting for message...")
        try:
            data, addr = udpServerSocket.recvfrom(BUFSIZ)
        except socket.timeout:
            return
        msg = data.decode('utf-8')
        print("receive msg:", msg)

        if msg == "quit":
            udpServerSocket.sendto("server is end".encode('utf-8'), addr)
            udpServerSocket.close()
            sys.exit(0)

        content = '[%s] %s' % (bytes(ctime(), 'utf-8'), msg)
        udpServerSocket.sendto(content.encode('utf-8'), addr)
        print('...received from and returned to:', addr)

try:
    udp_server()
except KeyboardInterrupt as e:
    udpServerSocket.close()
