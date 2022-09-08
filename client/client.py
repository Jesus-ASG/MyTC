import socket
import pickle
import os
import sys
import time
sys.path.append('..')
from structure import Structure

host = 'localhost'
port = 8000

os.system('cls' if os.name == 'nt' else 'clear')

l = list()


def listarTodo(path):
    files = os.listdir(path)
    for file in files:
        new_path = os.path.join(path, file)
        if os.path.isdir(new_path):
            # l.append(new_path)
            listarTodo(new_path)
        else:
            l.append(new_path)
    return l


path_files = listarTodo('share')
list_files = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    print('Connected to server')

    st = time.time()
    for fs in path_files:
        file = open(fs, 'rb')
        bin_data = file.read()
        obj = Structure(fs, bin_data)
        list_files.append(obj)
        print(f'Sending {fs}')

    send = pickle.dumps(list_files)
    s.send(send)

    en = time.time()
    ej = en - st
    print(f'files sent in {ej} s')
