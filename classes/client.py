import socket

class Client:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port

    # Подключение клиента к серверу
    def sendServer(self, cmd):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.__host, self.__port))
        conn.send(cmd.encode())

        data = conn.recv(1024)
        answer = data.decode()

        conn.close()
        return answer


