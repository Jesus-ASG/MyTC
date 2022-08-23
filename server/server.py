import socket

host = '192.168.100.151'
port = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()

    file = open('share/txt.txt', 'wb')
    
    l = conn.recv(1024)
    while(l):
        file.write(l)
        l = conn.recv(1024)
        
    file.close()
    
    s.close()