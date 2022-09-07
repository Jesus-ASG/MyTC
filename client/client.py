
import socket
import os
import sys
import pathlib
from tkinter.ttk import Separator

host1 = '192.168.100.151'  # ip del servidor
host = 'localhost'
port = 8000  # Puerto de envío

FORMAT = 'UTF-8'
message_separate = '<separate>'
message_eof = '<endoffile>'

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


#files = listarTodo('share/')
fs = 'share/file.mp4'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    file_data = fs +message_separate

    s.send(file_data.encode(FORMAT))
    print('name sended')

    with open(fs, 'rb') as f:
        data = f.read()
        s.send(data)
    print('file sended')
    s.send(message_eof.encode(FORMAT))
    print('confirmation sended')



    
    
