#! /usr/bin/env python
import random
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--seed", dest="seed", help="Random seed", default=1, type=int)
parser.add_argument("-l", "--length", dest="length", help="Simulated genome length", default=100000, type=int)
parser.add_argument("--repeat-length", dest="repeat_length", help="Simulated repeat length", default=1000, type=int)
parser.add_argument("--num-repeats", dest="num_repeats", help="Number of repeats", default=10, type=int)
parser.add_argument("--vary-by", dest="vary_by", help="Repeats vary by at most this many nucleotides", default=0, type=int)

args = parser.parse_args()

random.seed(args.seed)                  # make reproducible

nucl = ["A", "G", "C", "T"]

x = ["A"] + ["G"] + ["C"] + ["T"]
x = x*(args.length / 4)

y = ["A"] + ["G"] + ["C"] + ["T"]
y = y*(args.repeat_length / 4)

random.shuffle(x)
random.shuffle(y)

x = "".join(x)
y = "".join(y)

z = []
chunksize = len(x) / args.num_repeats
for i in range(0, len(x), chunksize):
    z.append(x[i:i+chunksize])
    z.append(y)

    for j in range(args.vary_by):
        repeat_edit_idx = random.randrange(0, len(y))
        z[-1] = z[-1][:repeat_edit_idx] + random.choice(nucl) + z[-1][repeat_edit_idx + 1:]

print '>repgenome\n%s\n' % "".join(z)
