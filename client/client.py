
import socket
import os
import sys
import pathlib

host = '192.168.100.151'  # ip del servidor
port = 8000  # Puerto de envío
key = '/090008765'

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

def writeSafely(path):
    if os.path.isdir(path):
        os.makedir('-p '+path)

    splited = path.split('/')

    index = 0
    for c in path[::-1]:
        if c == '/':
            break
        else:
            index -= 1


    if not os.path.exists(splited[-2]):
        os.makedir('-p '+0)
    pass


files = listarTodo('share')
# inp = input("Presiona 1 para salir: ")
# if inp == "1":
#     sys.exit()

i = 'share/file.mp4'
#for i in files:
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    
    file = open(i, 'rb')
    # manda el nombre del archivo
    i += key
    s.send(i.encode('UTF-8'))

        # manda el archivo
        
    s.sendfile(file)
        


"""
while True:
    inp = input("Presiona 1 para salir: ")
    if inp == "1":
        break
    
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        print('Enviando archivo')
        file = open('share', 'rb')
        # l = file.read(1024)
        # while l:
        #     s.send(l)
        #     l = file.read(1024)
        s.sendfile(file)
        s.close()
"""

