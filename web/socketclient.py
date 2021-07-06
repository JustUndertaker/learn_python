import socket
import time


host = '115.159.209.61'
port = 8081 
addr = (host, port)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 连接server
client.connect(addr)
# 向server发送数据
client.send(b'I am client')
# 接收server返回的数据
revcdata = client.recv(1024)
# 收到的数据都是bytes类型
print(revcdata.decode(encoding='utf-8'))
time.sleep(1)
client.close()
