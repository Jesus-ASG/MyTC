# Transferir archivos mediante sockets con python
## Descripción
Implementación de un cliente y servidor para transferir archivos usando sockets en python. <br>
Copia todo el contenido de una carpeta del cliente a una carpeta del servidor

## Instalación
* Tener python3 instalado
* En el servidor se cambia la variable 'host' por la ip de su máquina, hace lo mismo en el cliente
* En el cliente, escriba la ruta de la carpeta que desea copiar
* Inicie el servidor
* Inicie el cliente

## Procedimiento
Ubique la dirección ip de su servidor<br>
Windows

    ipconfig
    
Linux

    ifconfig

Cambie la variable 'host' en ambos archivos por la ip de su servidor <br>
![image](https://user-images.githubusercontent.com/106128245/189126926-d45469fa-187a-470f-8966-e9f14375c4ad.png)

Escriba la carpeta que se desea copiar en el archivo 'client.py'<br>
![image](https://user-images.githubusercontent.com/106128245/189126556-327790a3-5889-4fb0-aad1-776f2c9df621.png)

Ejecute su servidor

    python3 server.py
   
Ejecute su cliente

    python3 client.py

## Capturas

### Cliente (Linux)
![ss2](https://user-images.githubusercontent.com/106128245/189125050-545fce89-e88a-4abe-92e5-55c3196bbcfb.png)

![ss](https://user-images.githubusercontent.com/106128245/189123547-9ea1e931-1cb1-4f50-8497-7ce1142eb634.png)

### Servidor (Windows)
![image](https://user-images.githubusercontent.com/106128245/189123056-41b7aa2d-ca5e-47ed-a45b-d00462a08917.png)
![image](https://user-images.githubusercontent.com/106128245/189123974-7fd8d9ee-d44a-47b3-8fe8-4dc5baab9084.png)

