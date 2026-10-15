import os
import socket


def getURL(answer):
    """
    return the url from the client request
    :param answer:
    :return:
    """
    url = None
    line1 = answer.split('\r\n')[0]
    params = line1.split(' ')
    if len(params) == 3 and params[0] == 'GET' and params[2] == "HTTP/1.1":
        url = params[1]
    return url[1:]

server_sock = socket.socket()
server_sock.bind(("0.0.0.0", 80)) #'8080'
server_sock.listen(3)

while True:
    client_soc, addr = server_sock.accept()
    print(f"{addr[0]} - connected")

    try:
        data = client_soc.recv(1024).decode()
    except Exception as e:
        print(f"error in receive {str(e)}")
    else:
        print(data)
        url = getURL(data)
        if url:
            if os.path.isfile(url):
                with open(url, "rb") as f:
                    data = f.read().decode()

                ans = f"HTTP/1.1 200 OK\r\nContent-Length: {str(len(url))}\r\n\r\n{url}"
                data_info = f"HTTP/1.1 200 OK\r\nContent-Length: {str(len(data))}\r\n\r\n{data}"
                try:
                    client_soc.send(ans.encode())
                    client_soc.send(data_info.encode())
                except Exception as e:
                    print(f"error in send {str(e)}")

    print(f"{addr[0]} - disconnected")
    client_soc.close()