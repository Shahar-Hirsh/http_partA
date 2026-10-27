import socket
import os

def send_secret_post(msg):
    """
    builds and sends the answer for secret post
    :param msg: the message to send
    :type msg: str
    :return: none
    """
    ans = f"POST /ShaharServer?secret HTTP/1.1\r\nContent-Length: {str(len(msg))}\r\n\r\n{msg}"
    try:
        my_sock.send(ans.encode())
    except Exception as e:
        print(f"error in sending data {str(e)}")

def send_image_post(path, img_data):
    """
    builds and sends the answer for image post
    :param path: the path to the image
    :type path: str
    :param img_data: the image
    :return: none
    """
    ans = "POST /ShaharServer?img_name=" + path.split('\\')[-1] + " HTTP/1.1\r\nContent-Length: " + str(len(img_data)) +"\r\n\r\n"
    ans = ans.encode() + img_data
    my_sock.send(ans)

while True:
    my_sock = socket.socket()

    try:
        my_sock.connect(("127.0.0.1", 8080))
    except Exception as e:
        my_sock.close()
        exit(f"server is down - try again {str(e)}")

    msg = input("enter: 1 for secret, 2 for sending a photo and 3 to exit - ")
    if msg == '1':
        msg = input("enter a message to send - ")
        send_secret_post(msg)
    elif msg == '2':
        while True:
            msg = input("enter the path for the photo - ")
            if os.path.isfile(msg) and msg.split('.')[1] in["jpg","png","jpeg","bmp"]:
                with open(msg, "rb") as f:
                    file_data = f.read()
                send_image_post(msg,file_data)
                break
            print("sorry file doesn't exist/the file must be an image - try again")
    elif msg == '3':
        print("bye bye")
        my_sock.close()
        break
    else:
        print("not valid input - try again")

    my_sock.close()