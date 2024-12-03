import sys
from collections import Counter

import click


@click.group()
def cli():
    pass


@cli.command()
def day01():
    col1 = []
    col2 = []
    for line in sys.stdin:
        n1, n2 = map(int, line.strip().split())
        col1.append(n1)
        col2.append(n2)

    col1 = sorted(col1)
    col2 = sorted(col2)
    col2_counts = Counter(col2)

    total1 = 0
    for n1, n2 in zip(col1, col2):
        total1 += abs(n1 - n2)

    total2 = 0
    for n1 in col1:
        total2 += n1 * col2_counts[n1]

    print('Part 1:', total1)
    print('Part 2:', total2)


@cli.command()
def day02():
    def is_safe(report):
        diff = diff_sequence(report)
        is_inc = all(d > 0 for d in diff)
        is_dec = all(d < 0 for d in diff)
        in_range = all(1 <= abs(d) <= 3 for d in diff)
        return (is_inc or is_dec) and in_range

    def is_safe_dampened(report):
        return any(is_safe(omit(report, i)) for i in range(len(report)))

    num_safe = 0
    num_safe_dampened = 0

    for line in sys.stdin:
        report = [int(x) for x in line.strip().split()]
        num_safe += is_safe(report)
        num_safe_dampened += is_safe_dampened(report)

    print('Part 1:', num_safe)
    print('Part 2:', num_safe_dampened)


def diff_sequence(xs):
    return [y - x for x, y in zip(xs, xs[1:])]


def omit(xs, i):
    assert 0 <= i < len(xs)
    return xs[:i] + xs[i+1:]


if __name__ == "__main__":
    cli()
