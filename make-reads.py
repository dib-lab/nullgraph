#! /usr/bin/env python
from __future__ import print_function
import sys
import screed
import random
import screed
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--error-rate', type=float, default=.01)
parser.add_argument('-r', '--read-length', type=int, default=100,
                    help="Length of reads to generate")
parser.add_argument('-C', '--coverage', type=float, default=50.0,
                    help="Targeted coverage level")
parser.add_argument("-S", "--seed", dest="seed", help="Random seed", type=int,
                    default=1)
parser.add_argument("--even", dest="is_even", default=False,
                    action="store_true")
parser.add_argument("--mutation-details", dest="mutation_details", help="Write detailed log of mutations here")

parser.add_argument('genome')
args = parser.parse_args()

args = parser.parse_args()

COVERAGE=args.coverage
READLEN=args.read_length
ERROR_RATE=args.error_rate

random.seed(args.seed)                  # make this reproducible, please.

record = next(iter(screed.open(args.genome)))

genome = record.sequence
len_genome = len(genome)

print('genome size:', len_genome, file=sys.stderr)
print('coverage:', COVERAGE, file=sys.stderr)
print('readlen:', READLEN, file=sys.stderr)
print('error rate:', ERROR_RATE, file=sys.stderr)

n_reads = int(len_genome*COVERAGE / float(READLEN))
read_mutations = 0
total_mut = 0

nucl = ['a', 'c', 'g', 't']

print("Read in template genome {0} of length {1} from {2}".format(record["name"], len_genome, args.genome), file=sys.stderr)
print("Generating {0} reads of length {1} for a target coverage of {2} with a target error rate of {3}".format(n_reads, READLEN, COVERAGE, ERROR_RATE), file=sys.stderr)

if args.mutation_details != None:
    details_out = open(args.mutation_details, "w")
else:
    details_out = None

for i in range(n_reads):
    per_read_mutations = 0
    start = random.randint(0, len_genome - READLEN)
    read = genome[start:start + READLEN].upper()

    # reverse complement?
    is_rc = False
    if random.choice([0, 1]) == 0:
        is_rc = True
        read = screed.rc(read)

    # error?
    was_mut = False
    rc_flag = 'f'
    if is_rc:
        rc_flag = 'r'
    seq_name = "read{0}{1}".format(i, rc_flag)

    orig_read = read
    for _ in range(READLEN):
        if ERROR_RATE > 0:
            force = False
            while force or random.randint(1, int(1.0/ERROR_RATE)) == 1:
                force = False
                pos = random.randint(1, READLEN) - 1
                if args.is_even:
                    while pos % 2:
                        pos = random.randint(1, READLEN) - 1

                orig = orig_read[pos]
                new_base = random.choice(nucl)
                if orig.lower() == new_base:
                    force = True        # force a mutation
                    continue
                
                if details_out != None:
                    print("{0}\t{1}\t{2}\t{3}".format(seq_name,
                                                      pos, orig, new_base),
                          file=details_out)

                read = read[:pos] + new_base + read[pos+1:]
                was_mut = True
                total_mut += 1
                per_read_mutations += 1
                
    if was_mut:
        read_mutations += 1
    
    print('>{0} start={1},mutations={2}\n{3}'.format(seq_name, start, per_read_mutations, read))

print("%d of %d reads mutated; %d total mutations" % \
      (read_mutations, n_reads, total_mut),  file=sys.stderr)
