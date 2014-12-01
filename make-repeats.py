#! /usr/bin/env python
import random
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--length', type=int, default=1000,
                    help="Simulated repeat length")
parser.add_argument('-s', '--seed', type=int, default=1,
                    help="Random number seed")
parser.add_argument('-n', '--number', type=int, default=10,
                    help='# of repeat copies')
parser.add_argument('-e', '--divergence', type=float, default=.01,
                    help='divergence between repeats (per base)')
args = parser.parse_args()

LENGTH = args.length
NUM = args.number
DIVERGENCE=args.divergence

random.seed(args.seed)

print >>sys.stderr, 'Using random seed:', args.seed

nucl = ['A', 'C', 'G', 'T']
x = nucl * (args.length / 4)

random.shuffle(x)

base_repeat = "".join(x)

repeat_list = []
for i in range(NUM):
    n_mut = 0
    new_repeat = base_repeat

    if DIVERGENCE > 0:
        for _ in range(args.length):
            force = False
            while force or random.randint(1, int(1.0/DIVERGENCE)) == 1:
                force = False

                pos = random.randint(1, args.length) - 1
                new_base = random.choice(nucl)

                if new_repeat[pos] == new_base:
                    force = True                # force a mutation
                    continue

                new_repeat = new_repeat[:pos] + new_base + new_repeat[pos+1:]
                n_mut += 1

    print >>sys.stderr, "repeat %d - %d muts, for %.3f divergence" % \
          (i, n_mut, float(n_mut) / len(new_repeat))
    
    repeat_list.append(new_repeat)

for i, r in enumerate(repeat_list):
    print ">r%d\n%s" % (i + 1, r)
