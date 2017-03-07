import asyncio
import logging
import sys

from fibo import fib

SERVER_ADDRESS = ('localhost', 10000)

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(name)s: %(message)s',
    #filename='server.log',
    stream=sys.stderr,
)
log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()


def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')


class FiboServer(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log = logging.getLogger('FiboServer_{}_{}'.format(*self.address))
        self.log.info('Connection accepted')

    def data_received(self, data):
        self.log.debug('Received: {}'.format(int_from_bytes(data)))
        try:
            result = fib(int_from_bytes(data))
            self.transport.write(int_to_bytes(result))
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

