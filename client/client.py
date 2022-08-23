import socket

host = '192.168.100.151'  # ip del servidor
port = 8000  # Puerto de envío

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    print('Enviando archivo')
    file = open('share/txt.txt', 'rb')
    # l = file.read(1024)
    # while l:
    #     s.send(l)
    #     l = file.read(1024)
    s.sendfile(file)
    s.close()
