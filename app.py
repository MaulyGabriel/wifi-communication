from server import Server
from loguru import logger


class App:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        logger.info('Started server')
        server = Server(self.host, self.port)
        server.read_clients()


if __name__ == '__main__':
    app = App(host='172.16.2.124', port=9090)
    app.run()
