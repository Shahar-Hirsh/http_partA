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
server_sock.bind(("0.0.0.0", 8080)) #'8080'
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
        print("URL:", url)
        print("File exists:", os.path.isfile(url))
        if url:
            if os.path.isfile(url):
                with open(url, "rb") as f:
                    file_data = f.read()

                #ans = f"HTTP/1.1 200 OK\r\nContent-Length: {str(len(url.split('/')[-1]))}\r\n\r\n{url.split('/')[-1]}"
                data_info = f"HTTP/1.1 200 OK\r\nContent-Length: {str(len(file_data))}\r\n\r\n"
                try:
                    #client_soc.send(ans.encode())
                    client_soc.send(data_info.encode())
                    client_soc.send(file_data)
                except Exception as e:
                    print(f"error in send {str(e)}")
            else:
                ans = f"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
                try:
                    client_soc.send(ans.encode())
                except Exception as e:
                    print(f"error in send {str(e)}")

    print(f"{addr[0]} - disconnected")
    client_soc.close()