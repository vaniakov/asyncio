"""Fibobaccy function."""
import asyncio
import functools

passed = '\033[92m[OK]\033[0m'
failed = '\033[91m[FAILED]\033[0m'


async def fib_async(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a


async def main(loop, cases):
    for case in cases:
        inp, exp = case
        task = loop.create_task(functools.partial(fib_async, inp))
        got = await task
        result = passed if got == exp else failed
        print('fib({inp:^5}) expected: {exp:<5} got: {got:<5} {result: ^15}'.format(**locals()))


def fib(n):
    result = 0
    for num in _fig_gen(n):
        result = num
    return result


def _fig_gen(n):
    a, b = 0, 1
    for i in range(n):
        yield b
        a, b = b, a + b



if __name__ == '__main__':
    test_cases = ((0, 0), (1, 1), (2, 1), (3, 2), (4, 3),
                  (5, 5), (6, 8), (7, 13), (8, 21))
    print('Generator version testing:')
    for inp, exp in test_cases:
        got = fib(inp)
        result = passed if got == exp else failed
        print('fib({inp:^5}) expected: {exp:<5} got: {got:<5} {result: ^15}'.format(**locals()))

    print('Async version testing:')

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(event_loop, test_cases))
    finally:
        event_loop.close()
