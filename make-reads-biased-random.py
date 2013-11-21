#! /usr/bin/env python
import screed
import random
import fasta
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--mutation-details", dest="mutation_details", help="Write detailed log of mutations here")
parser.add_argument("--read-length", dest="read_length", help="Length of reads to generate", type=int, default=100)
parser.add_argument("--coverage", dest="coverage", help="Targeted coverage level", type=int, default=50)
parser.add_argument("--error-rate", dest="error_rate", help="Target error rate (1 base in X)", type=int, default=100)
parser.add_argument("-r", "--seed", dest="seed", help="Random seed", type=int, default=1)
parser.add_argument("input_file")

args = parser.parse_args()

random.seed(args.seed)                  # make this reproducible, please.

COVERAGE=args.coverage
READLEN=args.read_length
ERROR_RATE=args.error_rate

record = iter(screed.open(args.input_file)).next()
genome = record.sequence
len_genome = len(genome)

n_reads = int(len_genome*COVERAGE / float(READLEN))
reads_mut = 0
total_mut = 0

nucl = ['a', 'c', 'g', 't']

print >>sys.stderr, "Read in template genome {0} of length {1} from {2}".format(record["name"], len_genome, args.input_file)
print >>sys.stderr, "Generating {0} reads of length {1} for a target coverage of {2} with a target error rate of 1 in {3}".format(n_reads, READLEN, COVERAGE, ERROR_RATE)

if args.mutation_details != None:
    details_out = open(args.mutation_details, "w")
else:
    details_out = None

for i in range(n_reads):
    start = random.randint(0, len_genome - READLEN)
    read = genome[start:start + READLEN].upper()

    # reverse complement?
    if random.choice([0, 1]) == 0:
        read = fasta.rc(read)

    # error?
    was_mut = False
    seq_name = "read{0}".format(i)
    for _ in range(READLEN):
        while random.randint(1, ERROR_RATE) == 1:
            fake_end = int(READLEN*1.5)
            pos = random.randint(1, fake_end) - 1
            if pos >= READLEN:
                pos -= int(0.5 * READLEN)

            new_base = random.choice(nucl)
            orig = read[pos]

            if orig.lower() == new_base:
                continue

            if details_out != None:
                print >>details_out, "{0}\t{1}\t{2}\t{3}".format(seq_name, pos, orig, new_base)

            read = read[:pos] + new_base + read[pos+1:]
            was_mut = True
            total_mut += 1

    if was_mut:
        reads_mut += 1
    
    print '>{0}\n{1}'.format(seq_name, read)

print >>sys.stderr, "%d of %d reads mutated; %d total mutations" % \
    (reads_mut, n_reads, total_mut)
