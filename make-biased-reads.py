#! /usr/bin/env python
from __future__ import print_function
import screed
import sys
import random
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--error-rate', type=float, default=.01)
parser.add_argument('-r', '--read-length', type=int, default=100,
                    help="Length of reads to generate")
parser.add_argument('-C', '--coverage', type=int, default=50,
                    help="Targeted coverage level of first sequence")
parser.add_argument("-S", "--seed", dest="seed", help="Random seed", type=int,
                    default=1)
parser.add_argument("--mutation-details", dest="mutation_details", help="Write detailed log of mutations here")
parser.add_argument('genome')

args = parser.parse_args()

random.seed(args.seed)                  # make this reproducible, please.

COVERAGE = args.coverage
READLEN = args.read_length
ERROR_RATE = args.error_rate

# calculate number of reads to output from first sequence
record = next(iter(screed.open(args.genome)))

genome = record.sequence
len_genome = len(genome)

zero_index_count = int(len_genome*COVERAGE / float(READLEN))
nucl = ['a', 'c', 'g', 't']

####

if args.mutation_details != None:
    details_out = open(args.mutation_details, "w")
else:
    details_out = None

indices = []
seqs = []
powers = {}

index = 0
for r in screed.open(args.genome):
    description = r.name.split()[-1]
    power = float(description)
    count = int(math.pow(10, power))
    indices += [index] * count
    seqs.append(r.sequence)
    powers[index] = power

    print(r.name, power, count, file=sys.stderr)

    index += 1

reads_mut = 0
total_mut = 0

z = []
n_reads = 0
while zero_index_count > 0:
    index = random.choice(indices)
    if index == 0:
        zero_index_count -= 1

    sequence = seqs[index]

    start = random.randint(0, len(sequence) - READLEN)
    read = sequence[start:start + READLEN].upper()

    # reverse complement?
    if random.choice([0, 1]) == 0:
        read = screed.rc(read)

    seq_name = 'read%d' % (n_reads,)

    # error?
    was_mut = False
    for _ in range(READLEN):
        if ERROR_RATE > 0:
            while random.randint(1, int(1.0/ERROR_RATE)) == 1:
                pos = random.randint(1, READLEN) - 1
                orig = read[pos]
                new_base = random.choice(nucl)
                if orig.lower() == new_base:
                    continue

                if details_out != None:
                    print("{0}\t{1}\t{2}\t{3}".format(seq_name,
                                                      pos, orig, new_base),
                                                      file=sys.stderr)

                read = read[:pos] + new_base + read[pos+1:]
                was_mut = True
                total_mut += 1

    if was_mut:
        reads_mut += 1

    print('>%s\n%s' % (seq_name, read))
    z.append(index)
    n_reads += 1

y = []
for i in set(z):
    y.append((z.count(i), i))
y.sort()
print('reads per sequence:', y, file=sys.stderr)

print("%d of %d reads mutated; %d total mutations" % \
    (reads_mut, n_reads, total_mut), file=sys.stderr)
