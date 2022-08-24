import socket
import os

host1 = '192.168.100.151'
host = 'localhost'
port = 8000

os.system('cls' if os.name == 'nt' else 'clear')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen() # escuchando
    conn, addr = s.accept() 

    f_num = int(conn.recv(1024).decode('UTF-8'))
    conn.send('ok'.encode('UTF-8')) # confirmación de total de archivos
    
    for i in range(f_num):
        path = conn.recv(1024).decode('UTF-8') # recibe path
        print(f'{path}')

    """
    path = conn.recv(1024).decode('UTF-8') # recibe path
    print(f'recibido {path}')

    # obtiene el nombre del path
    filename = path.split('/')[-1]

    # obtiene el path separado
    path = path[:len(path)-len(filename)]

    # verifica si la ruta del path existe, si no la crea
    if not os.path.exists(path):
        os.makedirs(path)

    # crea el documento
    file = open(path+filename, 'wb')
    l = conn.recv(1024)
    while(l):
        file.write(l)
        l = conn.recv(1024)
        
    file.close()
    """