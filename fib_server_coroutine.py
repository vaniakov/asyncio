import asyncio
import logging
import sys
import ssl

import fibo

SERVER_ADDRESS = ('192.168.33.10', 10001)
# SSL does not support EOF, so send a null byte to indicate
# the end of the message.
EOF = b'\x00'


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(name)s: %(message)s',
    #filename='server.log',
    stream=sys.stderr,
)
log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()


async def fibo_handler(reader, writer):
    address = writer.get_extra_info('peername')
    log = logging.getLogger('fib_serv_{}_{}'.format(*address))
    log.debug('Connection accepted')

    while True:
        data = await reader.read(128)
        terminate = data.endswith(EOF)
        data = data.rstrip(EOF)

        if data:
            log.debug('Received {!r}'.format(data))
            try:
                result = fibo.fib(int(data.strip()))
                writer.write(str(result).encode('utf8'))
                await writer.drain()
                log.debug('Sent {!r}'.format(result))
            except TypeError:
                log.error('Could not convert data to int: %s', data)
            await writer.drain()
        if not data or terminate:
            log.debug('Closing..')
            writer.close()
            return

# The certificate is created with pymotw.com as the hostname,
# which will not match when the example code runs elsewhere,
# so disable hostname verification.
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.check_hostname = False
ssl_context.load_cert_chain('certs/pymotw.crt', 'certs/pymotw.key')

# Create the server and let the loop finish the coroutine before
# starting the real event loop.
factory = asyncio.start_server(fibo_handler, *SERVER_ADDRESS, ssl=ssl_context)
server = event_loop.run_until_complete(factory)
log.info('Starting up on {} port {}'.format(*SERVER_ADDRESS))


# Enter the event loop permanently to handle all connections.
try:
    event_loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    log.debug('Closing server...')
    server.close()
    event_loop.run_until_complete(server.wait_closed())
    log.debug('Closing event loop...')
    event_loop.close()
