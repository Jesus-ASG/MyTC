
import socket
import os
import sys
import pathlib

host1 = '192.168.100.151'  # ip del servidor
host = 'localhost'
port = 8000  # Puerto de envío

system = 'LINUX'
os.system('cls' if os.name == 'nt' else 'clear')

l = list()
def listarTodo(path):
    files = os.listdir(path)
    for file in files:
        new_path = os.path.join(path, file)
        
        if os.path.isdir(new_path):
            listarTodo(new_path)
        else:
            l.append(new_path)
    return l



files = listarTodo('share')
# inp = input("Presiona 1 para salir: ")
# if inp == "1":
#     sys.exit()
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    s.send(str(len(files)).encode('UTF-8'))
    msgc = s.recv(1024).decode('UTF-8')
    
    while True:
        if msgc == 'ok':
            for i in files:
                # manda el nombre del archivo
                s.send(i.encode('UTF-8'))
                print(f'{i} enviado')
                file = open(i, 'rb')
                # manda el archivo
                s.sendfile(file)
                file.close()

                while True:
                    endp = s.recv(1024).decode('UTF-8')
                    if endp == 'end':
                        break
                s.send('continua'.encode('UTF-8'))

        
            break
    
    
