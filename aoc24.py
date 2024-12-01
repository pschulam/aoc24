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


if __name__ == "__main__":
    cli()
