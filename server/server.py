import socket
import os

host1 = '192.168.100.151'
host = 'localhost'
port = 8000

FORMAT = 'UTF-8'
message_separate = '<separate>'
message_eof = '<endoffile>'


os.system('cls' if os.name == 'nt' else 'clear')

current_file = ''
data = ''
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen() # escuchando
    conn, addr = s.accept() 

    while True:
        #verify = conn.recv(1024)

        
        data += conn.recv(1024).decode(FORMAT)
        if message_separate in data:
            print('leyó el nombre del archivo')
            path = data.split(message_separate)[0]
            data = data.split(message_separate)[1]
            current_file = path
            
            # obtiene el nombre del path
            filename = path.split('/')[-1]

            # obtiene el path separado
            path = path[:len(path)-len(filename)]

            # verifica si la ruta del path existe, si no la crea
            if not os.path.exists(path):
                os.makedirs(path)
        
        print('itera')
        
        if message_eof in data:
            print('leyó final de archivo, cf ', current_file)
            data = data.split(message_eof)[0]
            # crea el documento
            
            file = open(current_file, 'wb')
            data = data.encode(FORMAT)
            #while data:
            file.write(data)
            file.close()

            break

    

    