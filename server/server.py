import socket
import os

host = '192.168.100.151'
port = 8000

os.system('cls' if os.name == 'nt' else 'clear')

files_number = 0

# Escuchando primera vez para contar archivos
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((host, port))
#     s.listen()
#     conn, addr = s.accept()

#     aux = conn.recv(1024).decode('UTF-8')
#     files_number = int(aux)

# print(f'total files: {files_number}')



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen() # escuchando
    conn, addr = s.accept() 
    
    path = conn.recv(1024).decode('UTF-8') # recibe path

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
        
    # file.close()
    