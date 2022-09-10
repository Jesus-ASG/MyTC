import socket
import pickle
import os
import sys
import time
sys.path.append('..')
from structure import Structure

host = '192.168.100.2'
host1 = 'localhost'
port = 8000
sep_system = ''
sep_new = '<<<separator>>>'
SO = 'WINDOWS' if os.name == 'nt' else 'LINUX'
if SO == 'WINDOWS':
    os.system('cls')
    sep_system = '\\'
else:
    os.system('clear')
    sep_system = '/'

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


path_files = listarTodo('share'+sep_system)
for i in range(len(path_files)):
    path_files[i] = path_files[i].replace(sep_system, sep_new)


list_files = []
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    print('Connected to server')

    st = time.time()
    for fs in path_files:
        fsd = fs.replace(sep_new, sep_system)  # ruta origina del archivo
        file = open(fsd, 'rb')
        bin_data = file.read()  # lee archivo en binario
        obj = Structure(fs, bin_data)  # escribe datos en un objeto
        list_files.append(obj)  # agrega ese objeto a una lista

        print(f'Sending {fsd}')  # muestra el archivo enviado

    send = pickle.dumps(list_files)  # convierte lista de objetos a binario
    s.send(send) # manda lista de objetos

    en = time.time()
    ej = en - st
    print(f'files sent in {ej} s')
