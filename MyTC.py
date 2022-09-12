import sys
import time
import tkinter as tk
from tkinter import ttk

import socket
import pickle
import threading
import os

from system_config import SystemConfig
from structure import Structure  # for load structure with pickle, NO REMOVE

# system variables
config = SystemConfig()
end_program = False
input_ip = None
input_port = None


l = list()


def list_dir(path):
    files = os.listdir(path)
    for file in files:
        new_path = os.path.join(path, file)
        if os.path.isdir(new_path):
            # l.append(new_path)
            list_dir(new_path)
        else:
            l.append(new_path)
    return l


def server_mode(ip, port):
    global input_ip, input_port
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.bind((ip, port))
    main_socket.listen()
    conn, addr = main_socket.accept()

    if addr[0] == config.IP:  # check client ip
        main_socket.close()  # if it's the same, switch to client mode
        client_mode(input_ip.get(), int(input_port.get()))
        return
    print(f'Server listen from {addr}')

    # # # continue receiving files normally # # #
    data = b''
    while True:
        packet = conn.recv(config.BUFFER_SIZE)
        if not packet: break
        data += packet

    list_files = pickle.loads(data)

    for fobj in list_files:
        # Get absolute file path
        fobj.fpath = fobj.fpath.replace(config.SEP_ENCODED, config.SEP_SYSTEM)

        # Replaces old dir (send/) with new dir (receive/)
        fobj.fpath = fobj.fpath.replace(config.ROOT_DIR, config.receive_path)

        # Get filename
        filename = fobj.fpath.split(config.SEP_SYSTEM)[-1]

        # Get only dir path
        fobj.fpath = fobj.fpath[:len(fobj.fpath) - len(filename)]

        # Create dir if not exists
        if not os.path.exists(fobj.fpath):
            os.makedirs(fobj.fpath)

        # Write file
        file = open(fobj.fpath + filename, 'wb')
        file.write(fobj.fdata)
        file.close()
        print(f'{fobj.fpath + filename} saved')

    # # # # # #
    main_socket.close()


def client_mode(ip, port):
    path_files = list_dir(config.send_path)
    list_files = []

    # # # Code for client # # #
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ret = main_socket.connect_ex((ip, port))
    if ret != 0:
        print('Failed to connect')
        return
    print('Connected to server')
    st = time.time()
    for fs in path_files:
        # Reads in binary
        file = open(fs, 'rb')
        bin_data = file.read()
        file.close()

        # Modify path for read by server socket
        fm = fs
        fm = fm[len(config.send_path):len(fm)]
        fm = config.ROOT_DIR + fm
        fm = fm.replace(config.SEP_SYSTEM, config.SEP_ENCODED)

        # Save into list
        obj = Structure(fm, bin_data)
        list_files.append(obj)

        print(f'{fs} sent')  # muestra el archivo enviado

    send = pickle.dumps(list_files)  # convierte lista de objetos a binario
    main_socket.send(send)  # manda lista de objetos
    # # # #
    en = time.time()
    ej = en - st
    print(f'Files sent in {ej}s')


def connect_function(ip, port):
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_socket.connect((ip, port))
    new_socket.close()


def main():
    global end_program, config, input_ip, input_port
    # get system configuration

    lbl_ip = config.IP
    # # # #

    root = tk.Tk()

    # Window settings
    s_width = root.winfo_screenwidth()
    s_height = root.winfo_screenheight()

    w_width = 700
    w_height = 400

    c_x = s_width // 2 - w_width // 2
    c_y = s_height // 2 - w_height // 2

    window_geometry = f'{w_width}x{w_height}+{c_x}+{c_y}'
    # # # #

    root.title('MyTC - My Tunnel Connector v1.0')
    ttk.Label(root, text='Bienvenido a MyTC').place(x=w_width//2-100, y=50)

    if lbl_ip:
        lbl_ip = 'PC information\nIP ADDRESS: ' + lbl_ip + '    PORT:' + str(config.PORT)
    else:
        lbl_ip = 'Couldn\'nt connect to internet :('
    ttk.Label(root, text=lbl_ip).place(x=50, y=100)

    ttk.Label(root, text='Send Directory Name: '+config.send_path+'/').place(x=50, y=150)
    ttk.Label(root, text='Receive Directory Name: ' + config.receive_path + '/').place(x=50, y=170)
    ttk.Label(root, text='IP ADDRESS:').place(x=50, y=250)
    input_ip = ttk.Entry()
    input_ip.place(x=150, y=250)
    ttk.Label(root, text='PORT:').place(x=340, y=250)
    input_port = ttk.Entry(width=10)
    input_port.place(x=400, y=250)

    thr_server = threading.Thread(target=server_mode, args=(config.IP, config.PORT))
    thr_server.start()

    ttk.Button(root, text='Send', command=lambda: connect_function(config.IP, config.PORT)).place(x=500, y=250)

    root.geometry(window_geometry)

    root.mainloop()
    # end_program = True


if __name__ == '__main__':
    main()
