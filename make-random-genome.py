#! /usr/bin/env python
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--seed", dest="seed", help="Random seed", default=1, type=int)
parser.add_argument("-l", "--length", dest="length", help="Simulated genome length", default=100000, type=int)

args = parser.parse_args()

random.seed(args.seed)                  # make reproducible

x = ["A"] + ["G"] + ["C"] + ["T"]
x = x*(args.length / 4)

random.shuffle(x)

print '>repgenome\n%s\n' % "".join(x)
