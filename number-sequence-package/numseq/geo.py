"""A collection geometry-related functions."""


def square(n):
    """returns (n) squared"""
    return n**2


def triangle(n):
    """returns (n) triangulated"""
    x = .5
    for j in range(n):
        x = x + .5
    return (n * x)


def cube(n):
    """returns (n) cubed"""
    return n**3
