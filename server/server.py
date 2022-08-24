import socket

host = '192.168.100.151'
port = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()

    resp = conn.recv(1024)
    if resp:
        print(resp.decode('utf-8'))

    # file = open('share', 'wb')
    
    # l = conn.recv(1024)
    # while(l):
    #     file.write(l)
    #     l = conn.recv(1024)
        
    # file.close()
    
    s.close()