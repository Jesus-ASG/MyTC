import socket
import os

host = '192.168.100.151'
port = 8000
key = '/090008765'

os.system('cls' if os.name == 'nt' else 'clear')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen() # escuchando
    conn, addr = s.accept() 
    
    full = conn.recv(1024).decode('UTF-8') # recibe datos completos

    # recorta hasta encontrar la llave
    path = ''
    for i in full:
        path += i
        if i == key:
            break
    
    # recorta el mensaje binario del de texto
    full = full[len(path):len(full)]
    #full = full.encode('UTF-8')

    # quita la llave del path
    path = path[:len(path)-len(key)]

    # obtiene el nombre del path
    filename = path.split('/')[-1]

    # obtiene el path separado
    path = path[:len(path)-len(filename)]

    # verifica si la ruta del path existe, si no la crea
    if not os.path.exists(path):
        os.makedirs(path)

    # crea el documento
    # full1 = conn.recv(1024)
    # print(full1.decode('UTF-8'))

    file = open(path+filename, 'wb')
    # file.write(bytes(full))
    #file.close()
    
    l = conn.recv(1024)
    while(l):
        file.write(l)
        l = conn.recv(1024)
        
    # file.close()
    