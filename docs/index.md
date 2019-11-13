# Solinftec -  Wifi Communication

<b>Desenvolvedor:</b> 

Gabriel Mauly (Madruga)

<b>Contato:</b>

(18) 98167-8570 | gabriel.mauly@solinftec.com.br | live:gabrielmaulysolinftec


## Solicitação:

Construir um servidor que seja capaz de enviar e receber dados através da comunicação wifi.

## Estrutura do projeto

    wifi-communication
        /docs           # documentação do projeto
        app.py          # arquivo main (o que faz acontecer kkk')
        mkdocs.yml      # arquivo de configuração da documentação
        server.py       # algoritmo que implementa o servidor wifi
        
 
## Desenvolvimento


### Linguagem e  Bibliotecas

O algoritmo foi desenvolvido na linguagem python, com sua versão <b>3.6</b>.
 
Utilizamos as seguintes bibliotecas nativas do python:
 
    socket, time, sys e os
 
E uma biblioteca de terceiro, para monitoramento de logs:
 
    loguru

Para realizar a instalação dessa biblioteca é muito simples, use:

    pip3 install loguru

### Implementação

Foram criadas duas classes, sendo elas: <b>App</b> e <b>Server</b>


<b>App (app.py) </b>

Responsável em executar o algoritmo, espera o endereço do host e a porta da conexão.

```python
# importando nossa classe Server
from server import Server

class App:

    
    def __init__(self, host, port):  
        """
        Nosso método construtor, espera:
       
        host: endereço IP do servidor
        port: número da porta de conexão
    
        """   
        self.host = host
        self.port = port

    def run(self):
        """
        Responsável por iniciar nosso servidor e realizar a 
        leitura das mensagens enviadas pelos clientes
        """
        server = Server(self.host, self.port)
        server.read_clients()


if __name__ == '__main__':
    """
    Iniciamos nosso servidor com os seguintes parâmetros: 
    host: 172.16.2.124  
    port: 9090    
    """
    app = App(host='172.16.2.124', port=9090)
    app.run()

```

<b>Server (server.py)</b>

Reponsável pela configuração do servidor e gerenciamento das mensagens recebidas.

```python

# importações necessárias
from loguru import logger
from time import sleep
import socket
import sys
import os


class Server:

    def __init__(self, host, port):
        """
        Nosso método construtor que espera o host e port passado no arquivo app.py.
        
        Temos algumas configurações a mais que reflete sobre o modo de 
        trabalho do nosso servidor.
        """
        self.host = host
        self.port = port
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.message = bytes(b"CLOSE CONNECTION\r\n")

    def open_connection(self):
        """
        Responsável por abrir a conexão do servidor.
        """

        try:
            origin = (self.host, self.port)
            self.tcp.bind(origin)
            self.tcp.listen(1)
        except OSError:
            logger.error('Error in connection')

    def read_clients(self):
        """
        Responsável por aceitar a conexão de cada cliente e exibir a 
        mensagem que cada um esta enviando.
        """

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

                    logger.error('Close connection: {} '.format(client))

                    con.close()
                    sys.exit(0)
                else:
                    con.close()

            except KeyboardInterrupt:
                con.sendall(self.message)
                sleep(1)
                con.close()
                logger.debug('End server')
                sys.exit(0)

            except TypeError:
                con.close()
                logger.debug('Type error in message')
                sys.exit(0)




```