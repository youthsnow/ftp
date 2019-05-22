"""
ftp　文件服务器
并发网络功能训练
"""

from socket import *
from threading import Thread
import os
from time import sleep

# 　全局变量
HOST = '0.0.0.0'
PORT = 8080
ADDR = (HOST, PORT)
FTP = "/home/tarena/FTP/"  # 文件库路径


# 将客户端请求功能封装为类
class FtpServer:
    def __init__(self, connfd, FTP_PATH):
        self.connfd = connfd
        self.path = FTP_PATH

    def do_list(self):
        #　获取文件列表
        files = os.listdir(self.path)
        if not files:
            self.connfd.send("该文件类别为空".encode())
            return
        else:
            self.connfd.send(b'OK')
            sleep(0.1)
        fs = ''
        for file in files:
            if file[0] != '.' and \
                    os.path.isfile(self.path+file):
                fs += file + '\n'
        self.connfd.send(fs.encode())


# 客户端请求处理函数
def handle(connfd):
    # 　选择文件夹
    cls = connfd.recv(1024).decode()
    FTP_PATH = FTP + cls + '/'
    ftp = FtpServer(connfd, FTP_PATH)
    while True:
        # 接受客户端请求
        data = connfd.recv(1024).decode()
        #　如果客户端断开返回ｄａｔａ为空
        if not data or data[0] == 'Q':
            return
        elif data[0] == 'L':
            ftp.do_list()


# 网络搭建
def main():
    # 　创建套接字
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(5)
    print("Listen the port 8080...")
    while True:
        try:
            connfd, addr = sockfd.accept()
        except KeyboardInterrupt:
            print("退出服务程序")
            return
        except Exception as e:
            print(e)
            continue
        print("链接的客户端：", addr)
        # 　创建线程处理请求
        client = Thread(target=handle, args=(connfd,))
        client.setDaemon(True)
        client.start()


if __name__ == "__main__":
    main()
