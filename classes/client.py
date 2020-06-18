import socket

class Client:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port

    def sendServer(self, cmd):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((self.__host, self.__port))
        conn.send(cmd.encode())
        conn.settimeout(0.2)

        answer = ""

        try:
            while True:
                data = conn.recv(1024)
                answer += data.decode()
                # print(data.decode(), end='')
        except socket.timeout:
            pass

        conn.close()
        return answer


