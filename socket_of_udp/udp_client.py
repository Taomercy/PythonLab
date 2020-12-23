import sys
from socket import *

HOST = '127.0.0.1'
PORT = 8888
BUFSIZ = 1024
ADDRESS = (HOST, PORT)

udpClientSocket = socket(AF_INET, SOCK_DGRAM)
udpClientSocket.settimeout(30.0)


def udp_client():
    while True:
        data = input('>')
        if not data:
            break

        # 发送数据
        udpClientSocket.sendto(data.encode('utf-8'), ADDRESS)
        # 接收数据
        try:
            data, ADDR = udpClientSocket.recvfrom(BUFSIZ)
        except timeout:
            return
        if not data:
            break
        print("server feedback:", data.decode('utf-8'))
        if data.decode('utf-8') == "server is end":
            sys.exit(0)

try:
    udp_client()
except KeyboardInterrupt as e:
    udpClientSocket.close()
