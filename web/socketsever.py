#!usr/bin/python
import socket

# 指定协议
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 让端口可以重复使用
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 绑定ip和端口
server.bind(('0.0.0.0', 8081))
# 监听
server.listen(1)
# 等待连接
clientsocket, address = server.accept()
# 接收消息
data = clientsocket.recv(1024)
clientsocket.send('我已经收到'.encode(encoding='utf-8'))
clientsocket.close()
server.close()