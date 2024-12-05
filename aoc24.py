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


@cli.command()
def day04():
    puzzle = [list(line.strip()) for line in sys.stdin]
    nrow = len(puzzle)
    ncol = len(puzzle[0])

    count1 = 0
    for y in range(nrow):
        for x in range(ncol):
            if puzzle[y][x] != 'X':
                continue
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    ys = [y + n*dy for n in range(4)]
                    xs = [x + n*dx for n in range(4)]
                    if any(y < 0 or y >= nrow for y in ys):
                        continue
                    if any(x < 0 or x >= ncol for x in xs):
                        continue
                    word = ''.join([puzzle[y][x] for y, x in zip(ys, xs)])
                    count1 += word == 'XMAS'

    count2 = 0
    for y in range(nrow):
        for x in range(ncol):
            if puzzle[y][x] != 'A':
                continue
            if y-1 < 0 or y+1 >= nrow or x-1 < 0 or x+1 >= ncol:
                continue
            corners = ''.join([
                puzzle[y + dy][x + dx]
                for dy, dx in [(-1, -1), (1, 1), (-1, 1), (1, -1)]
            ])
            count2 += (
                corners == 'MSMS'
                or
                corners == 'MSSM'
                or
                corners == 'SMMS'
                or
                corners == 'SMSM'
            )

    print('Part 1:', count1)
    print('Part 2:', count2)


def diff_sequence(xs):
    return [y - x for x, y in zip(xs, xs[1:])]


def omit(xs, i):
    assert 0 <= i < len(xs)
    return xs[:i] + xs[i+1:]


if __name__ == "__main__":
    cli()
