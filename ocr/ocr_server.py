import os
import socket  # Import socket module
from ocr import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
host = "localhost"  # Ip address that the TCPServer  is there
port = 1027  # Reserve a port for your service every new transfer wants a new port or you must wait.

server_address = (host, port)
sock.bind(server_address)

sock.listen(1)
while True:
    conn, addr = sock.accept()  # Establish connection with client.
    print('Got connection from', addr)
    data = conn.recv(1024)
    print('Server received', repr(data))
    filename = data.decode()
    _, file_extension = os.path.splitext(filename)
    if file_extension == '.pdf':
        filename = 'file.pdf'
    else:
        filename = 'file' + file_extension

    conn.send(b"Hello sender")
    with open(filename, 'wb') as f:
        print('file opened')
        while True:
            print('receiving data...')
            data = conn.recv(1024)
            print('data= ', data)
            if not data:
                break
            # write data to a file
            f.write(data)

    conn.close()

    if file_extension == '.pdf':
        pdf_reader(filename)
    else:
        image_reader(filename)


    conn, addr = sock.accept()

    data = conn.recv(1024)
    print('Server received', repr(data))

    filename = 'out_text.txt'
    f = open(filename, 'rb')
    l = f.read(1024)
    while l:
        conn.send(l)
        # print('Sent ', repr(l))
        l = f.read(1024)
    f.close()

    print('Done sending')
    # conn.send(b'Thank you for connecting')
    conn.close()
