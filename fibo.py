"""Fibobaccy function."""


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
    passed = '\033[92m[OK]\033[0m'
    failed = '\033[91m[FAILED]\033[0m'
    for inp, exp in test_cases:
        got = fib(inp)
        result = passed if got == exp else failed
        print('fib({inp:^5}) expected: {exp:<5} got: {got:<5} {result: ^15}'.format(**locals()))
