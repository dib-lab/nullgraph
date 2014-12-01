#! /usr/bin/env python
import random
import argparse
import sys
import screed

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--length', type=int, default=20000,
                    help="Total length of output genome")
parser.add_argument('-s', '--seed', type=int, default=1,
                    help="Random number seed")
parser.add_argument('input')
args = parser.parse_args()

LENGTH = args.length

nucl = ['A', 'C', 'G', 'T']

random.seed(args.seed)

print >>sys.stderr, 'Using random seed:', args.seed

seqs = [ r.sequence for r in screed.open(args.input) ]
input_length = sum([ len(s) for s in seqs ])
remainder = args.length - input_length

print >>sys.stderr, "final output should be: %d" % (args.length,)
print >>sys.stderr, "summed input: %d" % (input_length,)
print >>sys.stderr, "making: %d bp" % (remainder,)

assert remainder >= 0, remainder

random_len = remainder / (len(seqs) + 1)

print >>sys.stderr, "%d input seqs" % (len(seqs),)
print >>sys.stderr, "spacer len: %d" % (random_len,)

rest = []
for i in range(len(seqs) + 1):
    x = nucl * (random_len / 4)
    random.shuffle(x)
    rest.append("".join(x))

output = seqs + rest
print >>sys.stderr, len(output)
random.shuffle(output)

print '>remix\n%s' % ("".join(output))
