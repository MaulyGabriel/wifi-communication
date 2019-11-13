from loguru import logger
from time import sleep
import socket
import sys
import os


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.message = bytes(b"CLOSE CONNECTION\r\n")

    def open_connection(self):

        try:
            origin = (self.host, self.port)
            self.tcp.bind(origin)
            self.tcp.listen(1)
        except OSError:
            logger.error('Error in connection')

    def read_clients(self):

        self.open_connection()

        while True:

            con, client = self.tcp.accept()

            try:

                pid = os.fork()

                if pid == 0:
                    self.tcp.close()
                    logger.success('{} - Connected '.format(client))

                    while True:

                        msg = con.recv(1024)

                        if not msg:
                            break

                        logger.debug('Client {} send: {}'.format(client, msg))

                    logger.info('Close connection: {} '.format(client))

                    con.close()
                    sys.exit(0)
                else:
                    con.close()

            except KeyboardInterrupt:
                con.sendall(self.message)
                sleep(1)
                logger.debug('End server')
                con.close()
                sys.exit(0)

            except TypeError:
                logger.error('Type error in message')
                con.close()
                sys.exit(0)

            except ConnectionError:
                logger.error('Timeout connection')
