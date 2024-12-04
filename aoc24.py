import re
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


@cli.command()
def day03():
    instr_re = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
    cond_re = re.compile(r'do(n\'t)?\(\)')

    def add_muls(segment):
        return sum(int(x) * int(y) for x, y in instr_re.findall(segment))

    memory = sys.stdin.read()

    total1 = add_muls(memory)

    enabled = True
    curr = 0
    total2 = 0
    for match in cond_re.finditer(memory):
        m_start, m_end = match.span()
        if enabled:
            total2 += add_muls(memory[curr:m_start])
        enabled = match.group() == 'do()'
        curr = m_end
    if enabled:
        total2 += add_muls(memory[curr:])

    print('Part 1:', total1)
    print('Part 2:', total2)


def diff_sequence(xs):
    return [y - x for x, y in zip(xs, xs[1:])]


def omit(xs, i):
    assert 0 <= i < len(xs)
    return xs[:i] + xs[i+1:]


if __name__ == "__main__":
    cli()
