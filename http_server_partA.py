import os
import socket

def get_type(answer):
    """
    return the type of the client request
    :param answer:
    :return: the type of the request
    """
    type = None
    line1 = answer.split('\r\n')[0]
    params = line1.split(' ')
    if len(params) == 3  and params[2] == "HTTP/1.1":
        if params[0] == 'GET':
            type = 'GET'
        elif params[0] == 'POST':
            type = 'POST'
    return type

def getURL(answer):
    """
    return the url from the client request
    :param answer:
    :return:
    """
    url = None
    line1 = answer.split('\r\n')[0]
    params = line1.split(' ')
    if len(params) == 3 and (params[0] == 'GET' or params[0] == 'POST') and params[2] == "HTTP/1.1":
        url = params[1]
        if url == "/" and params[0] == 'GET':
            url = "/index.html" #index.html path

    if url is not None:
        url = url[1:]

    return url

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

def send_long_data(url):
    """
    sending the file data
    :param url:
    :return: none
    """
    with open(url, "rb") as f:
        file_data = f.read()

    # ans = f"HTTP/1.1 200 OK\r\nContent-Length: {str(len(url.split('/')[-1]))}\r\n\r\n{url.split('/')[-1]}"
    data_info = f"HTTP/1.1 200 OK\r\nContent-Length: {str(len(file_data))}\r\n\r\n"
    try:
        # client_soc.send(ans.encode())
        client_soc.send(data_info.encode())
        client_soc.send(file_data)
    except Exception as e:
        print(f"error in send {str(e)}")


def receives_data(headers ,data):
    """
    receives the rest of the data
    :param data: all the data
    :param headers: the headers of the data
    :return: all the data
    :rtype:
    """
    for line in headers.split('\r\n'):
        if line.startswith("Content-Length:"):
            params = line.split(' ')

    data = data.split(b"\r\n\r\n")[1]
    while len(data) < int(params[1]):
        slice = int(params[1]) - len(data)
        if slice > 1024:
            data += client_soc.recv(1024)
        else:
            data += client_soc.recv(slice)
            break
    return data

server_sock = socket.socket()
server_sock.bind(("0.0.0.0", 8080)) #'8080'
server_sock.listen(3)

moved_files = {"horse.jpg": "/horse2.jpg"}
no_access = ["pug.jpg","/pug.jpg"]
while True:
    client_soc, addr = server_sock.accept()
    print(f"{addr[0]} - connected")

    try:
        data = client_soc.recv(1024)
    except Exception as e:
        print(f"error in receive {str(e)}")
        print(f"{addr[0]} - disconnected")
        client_soc.close()
        continue


    headers = data.split(b'\r\n\r\n')[0].decode() # the headers of the data
    rec_type = get_type(headers)
    url = getURL(headers)

    if rec_type == 'GET':
        if url:
            if url.split("/")[-1] in no_access:
                ans = "HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\n\r\n"
                send_answer(ans)
            elif url in moved_files:
                ans = "HTTP/1.1 301 Moved Permanently\r\nLocation: " + moved_files[url] + "\r\nContent-Length: 0\r\n\r\n"
                send_answer(ans)
            elif url.lower() == "server":
                ans = "HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n"
                send_answer(ans)
            elif url.startswith("image?img-name=") and os.path.isfile(os.path.join("images", url.split('=')[1])):
                    send_long_data(os.path.join("images", url.split('=')[1]))

            elif os.path.isfile(url):
                send_long_data(url)

            elif url.lower().startswith("calculate-next"):
                if len(url) == len("calculate-next"):
                    num = 5
                    ans = f"HTTP/1.1 200 OK\r\nContent-Length: {str(len(str(num)))}\r\n\r\n{num}"
                elif url[len("calculate-next"):len("calculate-next?num=")] == "?num=":
                    try:
                        num = int(url[len("calculate-next?num="):])+1
                        ans = f"HTTP/1.1 200 OK\r\nContent-Length: {str(len(str(num)))}\r\n\r\n{num}"
                    except ValueError:
                        ans = f"HTTP/1.1 400 Bad Request\r\nContent-Length: {len('you need to enter a number')}\r\n\r\nyou need to enter a number"
                else:
                    ans = f"HTTP/1.1 400 Bad Request\r\nContent-Length: {len('you need to enter a number in num=')}\r\n\r\nyou need to enter a number in num="
                send_answer(ans)

            elif url.lower().startswith("calculate-area?"):
                if url.find("height=")<url.find("width="):
                    height = url[url.find("height=")+len("height="):url.find("&")]
                    width = url[url.find("&width=")+len("&width="):]
                else:
                    width = url[url.find("width=")+len("width="):url.find("&")]
                    height = url[url.find("&height=")+len("&height="):]

                if height.isdigit() and width.isdigit():
                    if int(height) > 0 and int(width) > 0:
                        area = int(width) * int(height) / 2
                        ans = f"HTTP/1.1 200 OK\r\nContent-Length: {str(len(str(area)))}\r\n\r\n{area}"
                    else:
                        ans = f"HTTP/1.1 400 Bad Request\r\nContent-Length: {'you need to enter numbers bigger than 0'}\r\n\r\nyou need to enter numbers bigger than 0"
                else:
                    ans = f"HTTP/1.1 400 Bad Request\r\nContent-Length: {'you need to enter numbers bigger than 0'}\r\n\r\nyou need to enter numbers bigger than 0"

                send_answer(ans)
            else:
                ans = f"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
                send_answer(ans)

    elif rec_type == 'POST':
        data = receives_data(headers,data)
        if url == "ShaharServer?secret":
            data = data.decode()
            print(data)
            with open("secret_messages.txt", "r") as f:
                messages = f.read()

            messages += data + "\n"

            with open("secret_messages.txt", "w") as f:
                f.write(messages)

        elif url.startswith("ShaharServer?img_name=") and url.split('.')[-1] in ["jpg","png","jpeg","bmp"]:
            with open(os.path.join('images', url.split('=')[-1]), "wb") as f:
                f.write(data)

    print(f"{addr[0]} - disconnected")
    client_soc.close()