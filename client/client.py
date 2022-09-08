import socket
import os
import math
import pickle
import sys

sys.path.append('..')
import pathlib
from tkinter.ttk import Separator

from structure import Structure

host1 = '192.168.100.151'  # ip del servidor
host = 'localhost'
port = 8000  # Puerto de envío

FORMAT = 'UTF-8'
message_separate = '<separate>'
message_eof = '<endoffile>'
pkg_size = 1024
fill_key = '|xfzd'

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


def send_package(s, pkg, pkg_size, encode):
    fill = ''
    if len(pkg + fill_key) < pkg_size:  # si el paquete es más chico que el tamaño
        num = (pkg_size - len(pkg + fill_key)) / len(fill_key)
        num = int(math.ceil(num))
        fill = fill_key * num  # lo completa
    else:
        fill = fill_key

    pkg += fill
    if encode:
        pkg = pkg.encode(FORMAT)
        # pkg = pkg[:pkg_size]

    s.send(pkg)


# files = listarTodo('share/')
fs = 'share/file.mp4'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    print('Connected to server')

    file = open(fs, 'rb')
    bin_data = file.read()
    obj = Structure(fs, bin_data)

    send = pickle.dumps(obj)
    s.send(send)

    print('file sent')
