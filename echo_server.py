import socket
import sys
import traceback


def server(log_buffer=sys.stderr):
    buffer_size = 16
    # set an address for our server
    address = ('127.0.0.1', 10000)

    # instantiate TCP socket with IPv4 Addressing
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    # TODO: You may find that if you repeatedly run the server script it fails,
    #       claiming that the port is already used.  You can set an option on
    #       your socket that will fix this problem. We DID NOT talk about this
    #       in class. Find the correct option by reading the very end of the
    #       socket library documentation:
    #       http://docs.python.org/3/library/socket.html#example

    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # bind socket to address and begin listening for incoming connections
    sock.bind(address)
    sock.listen(1)

    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)

            # wait for incoming connection and accept it
            conn, addr = sock.accept()

            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                while True:
                    # receive data from the client
                    data = conn.recv(buffer_size)
                    print('received "{0}"'.format(data.decode('utf8')))
                    
                    # send the data you received back to the client
                    conn.sendall(data)
                    print('sent "{0}"'.format(data.decode('utf8')))

                    if len(data) < buffer_size:
                        break
                    
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)

            finally:
                # close connection
                conn.close()
                print(
                    'echo complete, client connection closed', file=log_buffer
                )

    except KeyboardInterrupt: 
        # close server socket
        sock.close()
        print('quitting echo server', file=log_buffer)
        



if __name__ == '__main__':
    server()
    sys.exit(0)
