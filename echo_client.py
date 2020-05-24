import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    buffer_size = 16
    server_address = ('localhost', 10000)

    # instantiate a TCP socket with IPv4 Addressing
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)

    # connect socket to the server
    # sock.connect(("127.0.0.1", 10009))
    sock.connect(server_address)

    # variable to accumulate message received back from the server
    received_message = ''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        # send message to the server
        sock.sendall(msg.encode('utf-8'))

        while True:
            # receive chunk of message from server
            chunk = sock.recv(buffer_size)
            print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)

            # append chunk of message to received message
            received_message += chunk.decode('utf8')

            # check if end of message received
            if len(chunk) < buffer_size:
                break

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

    finally:
        # close client socket
        sock.close()
        print('closing socket', file=log_buffer)

        return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
