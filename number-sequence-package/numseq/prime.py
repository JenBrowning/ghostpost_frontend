"""A collection prime-related functions."""


def is_prime(n):
    """returns a boolean indicating whether (m) is prime"""
    if n >= 2:
        for y in range(2, n):
            if not (n % y):
                return False
    else:
        return False
    return True


def primes(n):
    """returns a list of primes less than (n)"""
    primes = []
    for num in range(2, n):
        if is_prime(num):
            primes.append(num)
    return primes
