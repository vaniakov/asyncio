import asyncio
import logging
import sys
import ssl

SERVER_ADDRESS = ('192.168.33.10', 10001)
# SSL does not support EOF, so send a null byte to indicate
# the end of the message.
EOF = b'\x00'

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(name)s: %(message)s',
    stream=sys.stderr,
)
log = logging.getLogger('main')

event_loop = asyncio.get_event_loop()


async def fib_client(address, messages):
    log = logging.getLogger('fib_client')
    log.debug('Connecting to {} port {}'.format(*address))

    # The certificate is created with pymotw.com as the hostname,
    # which will not match when the example code runs
    # elsewhere, so disable hostname verification.
    ssl_context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH,
    )
    ssl_context.check_hostname = False
    ssl_context.load_verify_locations('certs/pymotw.crt')
    reader, writer = await asyncio.open_connection(*address, ssl=ssl_context)
    for msg in messages:
        writer.write(str(msg).encode('utf8'))
        log.info('Sending {!r}'.format(msg))
        await writer.drain()
        data = await reader.read(128)
        if data:
            log.info('Received {!r}'.format(data))

        writer.write(EOF)
        await writer.drain()

    log.debug('Waiting for response')
    while True:
        data = await reader.read(128)
        if data:
            log.debug('Received {!r}'.format(data))
        else:
            log.debug('Closing..')
            writer.close()
            return

if len(sys.argv) > 1:
    try:
        event_loop.run_until_complete(fib_client(SERVER_ADDRESS, map(int, sys.argv[1:])))
    finally:
        log.debug('Closing event loop')
        event_loop.close()
