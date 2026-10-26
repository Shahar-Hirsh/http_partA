import socket
import os

def send_secret_post(msg):
    """
    builds and sends the answer for secret post
    :param msg: the message to send
    :type msg: str
    :return: none 
    """
    ans = "POST /ShaharServer?secret HTTP/1.1\r\nContent-Length: " +str(len(msg))+"\r\n\r\n" + msg
    try:
        my_sock.send(ans.encode())
    except Exception as e:
        print(f"error in sending data {str(e)}")

my_sock = socket.socket()
try:
    my_sock.connect(("127.0.0.1",8080))
except Exception as e:
    my_sock.close()
    exit(f"server is down - try again {str(e)}")

while True:
    msg = input("enter: 1 for secret, 2 for sending a photo and 3 to exit")
    if msg == '1':
        msg = input("enter a message to send")
    send_secret_post(msg)