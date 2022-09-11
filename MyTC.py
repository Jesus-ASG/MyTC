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
mode_server = b'<<<server>>>'
mode_client = b'<<<client>>>'
end_program = False


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
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.bind((ip, port))
    main_socket.listen()
    print('Server listen...')
    conn, addr = main_socket.accept()
    print(addr)

    if addr[0] == config.IP:  # check client ip
        main_socket.close()  # if it's the same, switch to client mode
        client_mode(ip, port)
        return

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
        print(f'Server: {fobj.fpath + filename} saved')

    # # # # # #
    main_socket.close()


def client_mode(ip, port):
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.connect((ip, port))



def connect_function(ip, port):
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    new_socket.connect((ip, port))
    new_socket.close()


def main():
    global end_program, config
    # get system configuration

    lbl_ip = config.IP
    # # # #

    root = tk.Tk()

    # Window settings
    s_width = root.winfo_screenwidth()
    s_height = root.winfo_screenheight()

    w_width = 700
    w_height = 600

    c_x = s_width // 2 - w_width // 2
    c_y = s_height // 2 - w_height // 2

    window_geometry = f'{w_width}x{w_height}+{c_x}+{c_y}'
    # # # #

    root.title('MyTC')
    lbl_welcome = tk.Label(root, text='Bienvenido a MyTC')
    lbl_welcome.place(x=5, y=5)

    if lbl_ip:
        lbl_ip = 'Your ip direction: ' + lbl_ip + ':' + str(config.PORT)
    else:
        lbl_ip = 'Couldn\'nt connect to internet :('
    lbl_ip = tk.Label(root, text=lbl_ip)
    lbl_ip.place(x=5, y=25)

    ttk.Label(root, text='Connect to').place(x=5, y=50)
    ttk.Label(root, text='IP:').place(x=100, y=50)
    input_ip = ttk.Entry()
    input_ip.place(x=130, y=50)
    ttk.Label(root, text='PORT:').place(x=310, y=50)
    input_port = ttk.Entry()
    input_port.place(x=360, y=50)

    thr_server = threading.Thread(target=server_mode, args=(config.IP, config.PORT))
    thr_server.start()

    ttk.Button(root, text='Connect', command=lambda: connect_function(config.IP, config.PORT)).place(x=530, y=50)

    root.geometry(window_geometry)

    root.mainloop()
    # end_program = True


if __name__ == '__main__':
    main()
