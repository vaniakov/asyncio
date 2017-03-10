import asyncio
import functools
import logging
import sys

MESSAGES = [1, 5, 10, 15, 30]

SERVER_ADDRESS = ('192.168.33.10', 10000)

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(name)s %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()


class FiboClient(asyncio.Protocol):

    def __init__(self, messages, future):
        super().__init__()
        self.messages = messages
        self.log = logging.getLogger('FiboClient')
        self.f = future

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.log.info(
            'Connecting to {} port {}'.format(*self.address)
        )
        # This could be transport.writelines() except that
        # would make it harder to show each part of the message
        # being sent.
        for msg in self.messages:
            transport.write(str(msg).encode('utf8'))
            transport.write(b' ')
            self.log.debug('Sending {!r}'.format(msg))
        if transport.can_write_eof():
            transport.write_eof()

    def data_received(self, data):
        self.log.info('Received {!r}'.format(data))

    def eof_received(self):
        self.log.debug('Received EOF')
        self.transport.close()
        if not self.f.done():
            self.f.set_result(True)

    def connection_lost(self, exc):
        self.log.debug('Server closed connection')
        self.transport.close()
        if not self.f.done():
            self.f.set_result(True)
        super().connection_lost(exc)


if __name__ == '__main__':
    client_completed = asyncio.Future()

    client_factory = functools.partial(
        FiboClient,
        messages=MESSAGES,
        future=client_completed
    )
    factory_coroutine = event_loop.create_connection(
        client_factory,
        *SERVER_ADDRESS
    )
    log.debug('Waiting for client to complete')
    try:
        event_loop.run_until_complete(factory_coroutine)
        event_loop.run_until_complete(client_completed)
    finally:
        log.debug('Closing event loop')
        event_loop.close()
