import sys
import time
import tkinter as tk
from tkinter import ttk

import socket
import pickle
import threading
import os
import configparser

from system_config import SystemConfig
from structure import Structure  # for load structure with pickle, NO REMOVE

# system variables
config = SystemConfig()
end_program = False
input_ip = None
input_port = None

# control variables
is_server = False
is_client = False

l = list()

# tkinter
root = tk.Tk()

# create files if not exists
if not os.path.exists(config.send_path):
    os.makedirs(config.send_path)

if not os.path.exists(config.receive_path):
    os.makedirs(config.receive_path)


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
    global input_ip, input_port, is_server, is_client, root
    is_server = True
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.bind((ip, port))
    main_socket.listen()
    conn, addr = main_socket.accept()

    if addr[0] == config.IP:  # check client ip
        main_socket.close()  # if it's the same, switch to client mode
        is_server = False
        if is_client:
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
    # Close socket
    main_socket.close()
    # Open socket for loop
    server_mode(ip, port)


def client_mode(ip, port):
    global root
    path_files = list_dir(config.send_path)
    list_files = []

    # Updating data
    write_config = configparser.ConfigParser()
    write_config['GENERAL'] = {
        'port': config.PORT,
        'receive_path': config.receive_path,
        'send_path': config.send_path
    }
    write_config['ADDRESS'] = {
        'last_ip': ip,
        'last_port': str(port)
    }

    with open('config.ini', 'w') as configfile:
        write_config.write(configfile)

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


def connect_function(ip, port, client_bool):
    global is_client
    is_client = client_bool
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_socket.connect((ip, port))
    new_socket.close()


def close(root):
    root.destroy()
    connect_function(config.IP, config.PORT, False)
    pass


def main():
    global end_program, config, input_ip, input_port, root
    # get system configuration

    lbl_ip = config.IP
    # # # #

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
    ttk.Label(root, text='Bienvenido a MyTC').place(x=w_width // 2 - 100, y=50)

    if lbl_ip:
        lbl_ip = 'PC information\nIP ADDRESS: ' + lbl_ip + '    PORT:' + str(config.PORT)
    else:
        lbl_ip = 'Couldn\'nt connect to internet :('
    ttk.Label(root, text=lbl_ip).place(x=50, y=100)

    ttk.Label(root, text='Send Directory Name: ' + config.send_path + '/').place(x=50, y=150)
    ttk.Label(root, text='Receive Directory Name: ' + config.receive_path + '/').place(x=50, y=170)
    ttk.Label(root, text='IP ADDRESS:').place(x=50, y=250)
    input_ip = ttk.Entry()
    input_ip.insert(0, config.last_ip)
    input_ip.place(x=150, y=250)
    ttk.Label(root, text='PORT:').place(x=340, y=250)
    input_port = ttk.Entry(width=10)
    input_port.insert(0, config.last_port)
    input_port.place(x=400, y=250)

    # starting peer in mode server
    thr_server = threading.Thread(target=server_mode, args=(config.IP, config.PORT))
    thr_server.start()

    # if clicks 'send' cancel server and join in mode client
    ttk.Button(root, text='Send', command=lambda: connect_function(config.IP, config.PORT, True)).place(x=500, y=250)

    root.geometry(window_geometry)
    root.protocol('WM_DELETE_WINDOW', lambda: close(root))

    root.mainloop()
    # end_program = True


if __name__ == '__main__':
    main()
