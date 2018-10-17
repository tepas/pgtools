import os
import math
import sys
import numpy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output")
args = parser.parse_args()

def Rx(theta):
    return numpy.array([
        [1.0,               0.0,                0.0],
        [0.0,               math.cos(theta),    -math.sin(theta)],
        [0.0,               math.sin(theta),    math.cos(theta)]
    ])

def Ry(theta):
    return numpy.array([
        [math.cos(theta),   0.0,                math.sin(theta)],
        [0.0,               1.0,                0.0],
        [-math.sin(theta),  0.0,                math.cos(theta)]
    ])

def Rz(theta):
    return numpy.array([
        [math.cos(theta),   -math.sin(theta),   0.0],
        [math.sin(theta),   math.cos(theta),    0.0],
        [0.0,               0.0,                1.0],
    ])

with open(args.input) as input_file:
    with open(args.output, 'w') as output_file:
        for line in input_file:
            line = line.strip()

            (typ, *args) = line.strip().split(' ')

            if typ == 'v':
                v = numpy.array([float(x) for x in args])
                v = v @ Rx(numpy.deg2rad(45))

                line = 'v %f %f %f' % (v[0], v[1], v[2])

            print(line, file=output_file)