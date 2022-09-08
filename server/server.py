import os
import pickle
import socket
import sys

sys.path.append('..')

from structure import Structure


host1 = '192.168.100.151'
host = 'localhost'
port = 8000

FORMAT = 'UTF-8'
message_separate = '<separate>'
message_eof = '<endoffile>'
pkg_size = 1024
fill_key = '|xfzd'

os.system('cls' if os.name == 'nt' else 'clear')

current_file = ''
data_aux = ''
data_b = ''
endoffile = False


it = 0
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print('Server listen...')
    conn, addr = s.accept()

    data = b''
    while True:
        packet = conn.recv(4096)
        if not packet: break
        data += packet

    d = pickle.loads(data)

    # obtiene el nombre del path
    filename = d.fpath.split('/')[-1]

    # obtiene el path separado
    d.fpath = d.fpath[:len(d.fpath) - len(filename)]

    # verifica si la ruta del path existe, si no la crea
    if not os.path.exists(d.fpath):
        os.makedirs(d.fpath)

    file = open(d.fpath+filename, 'wb')
    file.write(d.fdata)
    file.close()
    print(f'Server: {d.fpath} saved')
