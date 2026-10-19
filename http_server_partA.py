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
    if url == "/":
        url = "/index.html" #index.html path


    return url[1:]

def send_answer(answer):
    """
    sending the short answers
    :param answer: the answer to send
    :type answer: str
    :return: none
    """
    try:
        client_soc.send(answer.encode())
    except Exception as e:
        print(f"error in send {str(e)}")


server_sock = socket.socket()
server_sock.bind(("0.0.0.0", 8080)) #'8080'
server_sock.listen(3)

moved_files = {"horse.jpg": "/horse2.jpg"}
no_access = ["C:/Users/User/Desktop/computer/Cyber/http_partA/me.png"]
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
            if url in no_access:
                ans = "HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\n\r\n"
                send_answer(ans)
            elif url in moved_files:
                ans = "HTTP/1.1 301 Moved Permanently\r\nLocation: " + moved_files[url] + "\r\nContent-Length: 0\r\n\r\n"
                send_answer(ans)
            elif url.lower() == "server":
                ans = "HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n"
                send_answer(ans)
            elif os.path.isfile(url):
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

            elif url.lower().startswith("calculate-next"):
                if url[len("calculate-next"):len("calculate-next")+len("?num=")] == "?num=":
                    try:
                        num = int(url[len("calculate-next?num="):])+1
                        ans = f"HTTP/1.1 200 OK\r\nContent-Length: {str(len(str(num)))}\r\n\r\n{num}"
                    except ValueError:
                        ans = f"HTTP/1.1 400 Bad Request\r\nContent-Length: {len('you need to enter a number')}\r\n\r\nyou need to enter a number"
                else:
                    ans = f"HTTP/1.1 200 OK\r\nContent-Length: 1\r\n\r\n5"
                send_answer(ans)
            else:
                ans = f"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
                send_answer(ans)

    print(f"{addr[0]} - disconnected")
    client_soc.close()