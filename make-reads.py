#! /usr/bin/env python
import screed
import sys
import random
import fasta

random.seed(1)                  # make this reproducible, please.

COVERAGE=50
READLEN=100
ERROR_RATE=100

record = iter(screed.open(sys.argv[1])).next()
genome = record.sequence
len_genome = len(genome)

n_reads = int(len_genome*COVERAGE / float(READLEN))
reads_mut = 0
total_mut = 0

nucl = ['a', 'c', 'g', 't']

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
           pos = random.randint(1, READLEN) - 1

           new_base = random.choice(nucl)
           orig = read[pos]

           if orig.lower() == new_base:
               continue

           print >>sys.stderr, "{0}\t{1}\t{2}\t{3}".format(seq_name, pos, orig, new_base)

           read = read[:pos] + new_base + read[pos+1:]
           was_mut = True
           total_mut += 1

    if was_mut:
        reads_mut += 1
    
    print '>{0}\n{1}'.format(seq_name, read)

print >>sys.stderr, "%d of %d reads mutated; %d total mutations" % \
    (reads_mut, n_reads, total_mut)
