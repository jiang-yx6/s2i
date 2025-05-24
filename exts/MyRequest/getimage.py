import socket
import os
from django.conf import settings
def send_message_and_receive_image(host, port, message):
    # 创建一个 TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))

        # 发送消息
        client_socket.sendall(message.encode('utf-8'))

        # 接收图片数据
        image_data = b''
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            image_data += chunk

        directory = os.path.join(settings.MEDIA_ROOT, 'voice')
        save_path = os.path.join(directory, 'output.jpg')
        with open(save_path, 'wb') as f:
            f.write(image_data)

        return save_path