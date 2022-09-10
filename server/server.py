import socket
import pickle
import os
import sys
import time
sys.path.append('..')
from structure import Structure

host1 = 'localhost'
host = '192.168.100.151'
port = 8000

BUFFER_SIZE = 1048576

sep_system = ''
sep_new = '<<<separator>>>'
SO = 'WINDOWS' if os.name == 'nt' else 'LINUX'
if SO == 'WINDOWS':
    os.system('cls')
    sep_system = '\\'
else:
    os.system('clear')
    sep_system = '/'


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
        f_obj.fpath = f_obj.fpath.replace(sep_new, sep_system)
        filename = f_obj.fpath.split(sep_system)[-1]

        # obtiene el path separado
        f_obj.fpath = f_obj.fpath[:len(f_obj.fpath) - len(filename)]

        # verifica si la ruta del path existe, si no la crea
        if not os.path.exists(f_obj.fpath):
            os.makedirs(f_obj.fpath)

        file = open(f_obj.fpath + filename, 'wb')
        file.write(f_obj.fdata)
        file.close()
        print(f'Server: {f_obj.fpath+filename} saved')
