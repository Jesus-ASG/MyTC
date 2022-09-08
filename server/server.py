import socket
import pickle
import os
import sys
import time
sys.path.append('..')
from structure import Structure

host = 'localhost'
port = 8000

BUFFER_SIZE = 1048576

os.system('cls' if os.name == 'nt' else 'clear')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print('Server listen...')
    conn, addr = s.accept()

    data = b''
    while True:
        packet = conn.recv(BUFFER_SIZE)
        if not packet: break
        data += packet

    list_files = pickle.loads(data)

    for f_obj in list_files:
        # obtiene el nombre del path
        filename = f_obj.fpath.split('/')[-1]

        # obtiene el path separado
        f_obj.fpath = f_obj.fpath[:len(f_obj.fpath) - len(filename)]

        # verifica si la ruta del path existe, si no la crea
        if not os.path.exists(f_obj.fpath):
            os.makedirs(f_obj.fpath)

        file = open(f_obj.fpath + filename, 'wb')
        file.write(f_obj.fdata)
        file.close()
        print(f'Server: {f_obj.fpath+filename} saved')
