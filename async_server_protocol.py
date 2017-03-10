import asyncio
import logging
import sys

from fibo import fib

SERVER_ADDRESS = ('192.168.33.10', 10000)

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(name)s: %(message)s',
    #filename='server.log',
    stream=sys.stderr,
)
log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()


class FiboServer(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log = logging.getLogger('FiboServer_{}_{}'.format(*self.address))
        self.log.info('Connection accepted')

    def data_received(self, data):
        self.log.debug('Received: {}'.format(data))
        if not data.strip():
            return
        try:
            digits = data.split(b' ')
            result = [fib(int(digit)) for digit in digits if digit.isdigit()]
            for digit in result:
                self.transport.write(str(digit).encode('utf8'))
                self.transport.write(b'\n')
            self.log.debug('Sent: {}'.format(result))
        except TypeError as e:
            error_message = 'Can`t convert received data to int!'
            self.log.error(error_message)
            self.transport.write(error_message)

    def eof_received(self):
        self.log.debug('Received OEF')
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, error):
        if error:
            self.log.error(error)
        else:
            self.log.debug('Closing connection...')
        super().connection_lost(error)


factory = event_loop.create_server(FiboServer, *SERVER_ADDRESS)
server = event_loop.run_until_complete(factory)
log.info('Starting up on {} port {}'.format(*SERVER_ADDRESS))

try:
    event_loop.run_forever()
finally:
    log.info('Closing server...')
    server.close()
    event_loop.run_until_complete(server.wait_closed())
    log.debug('Closing event loop...')
    event_loop.close()

