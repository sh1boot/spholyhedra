#!/bin/env python3
# Needs: https://pypi.org/project/sdflab/
# (`pip install sdflab`, not `pip install sdf`)
from sdf import *
from sdf.d3 import sdf3, ORIGIN
import argparse
import math

def psum(*args, e=1):
    return sum(map(lambda x: pow(abs(x), e), args))

@sdf3
def tetrasphedron(radius=1, e=4, centre=ORIGIN):
    dihedral = math.acos(1 / 3)
    hs = math.sin(dihedral / 2) / 2
    hc = math.cos(dihedral / 2) / 2
    def f(p):
        p = (p - centre) / radius
        px, py, pz = p[:,0], p[:,1], p[:,2]
        x = hs * px
        y = hc * py
        z = hc * pz
        return psum(
                .5 + x + y,
                .5 + x - y,
                .5 - x + z,
                .5 - x - z,
                e=e
        ) - 1.0
    return f

@sdf3
def sphube(radius=1, e=4, centre=ORIGIN):
    def f(p):
        p = (p - centre) / radius
        px, py, pz = p[:,0], p[:,1], p[:,2]
        return psum(px, py, pz, e=e) - 1.0
    return f

def _octasphedron(radius=1, e=6, centre=ORIGIN):
    radius *= math.sqrt(3)
    def f(p):
        p = (p - centre) / radius
        px, py, pz = p[:,0], p[:,1], p[:,2]
        return psum(
                px + py + pz,
                px + py - pz,
                px - py + pz,
                px - py - pz,
                e=e
        ) - 1.0
    return f

@sdf3
def octasphedron(radius=1, e=6, centre=ORIGIN):
    return _octasphedron(radius=radius, e=e, centre=centre)

@sdf3
def dodecasphedron(radius=1, e=9, centre=ORIGIN):
    dihedral = math.acos(math.sqrt(5) / -5)
    c = math.cos(dihedral / 2)
    s = math.sin(dihedral / 2)
    def f(p):
        p = (p - centre) / radius
        px, py, pz = p[:,0], p[:,1], p[:,2]
        return psum(
               s * px + c * py,
               s * px - c * py,
               s * py + c * pz,
               s * py - c * pz,
               s * pz + c * px,
               s * pz - c * px,
               e=e
        ) - 1.0
    return f

@sdf3
def icosasphedron(radius=1, e=9, centre=ORIGIN):
    dihedral = math.acos(math.sqrt(5) / -3)
    c = math.cos(dihedral / 2)
    s = math.sin(dihedral / 2)
    octa = _octasphedron(radius=1, e=e, centre=ORIGIN)
    def f(p):
        p = (p - centre) / radius
        px, py, pz = p[:,0], p[:,1], p[:,2]
        return psum(
               s * px + c * py,
               s * px - c * py,
               s * py + c * pz,
               s * py - c * pz,
               s * pz + c * px,
               s * pz - c * px,
               e=e
        ) + octa(p)
    return f

def main():
    parser = argparse.ArgumentParser(description="Make an stl file")
    parser.add_argument('-s', '--shape', type=str, default='cube',
            choices=['tetrahedron', 'cube', 'hexahedron', 'octahedron', 'dodecahedron', 'icosahedron'],
            help="Name of the shape.")
    parser.add_argument('-e', '--exponent', type=float, default=4.0, help="exponent")
    parser.add_argument('-p', '--step', type=float, default=0.25, help="sampling step size")
    parser.add_argument('-o', '--output', type=str, default="out.stl", help="output file name")
    args = parser.parse_args()
    radius = 10
    bounds = ((-20, -20, -20), (20, 20, 20))

    match args.shape.lower():
        case '4' | 'tetrahedron':
            solid = tetrasphedron(radius, args.exponent)
        case '6' | 'cube' | 'hexahedron':
            solid = sphube(radius, args.exponent)
        case '8' | 'octahedron':
            solid = octasphedron(radius, args.exponent)
        case '12' | 'dodecahedron':
            solid = dodecasphedron(radius, args.exponent)
        case '20' | 'icosahedron':
            solid = icosasphedron(radius, args.exponent)
        case '_':
            exit(-1)

    solid.save(args.output, step=args.step, bounds=bounds)
    print(f"Saved to: {args.output}")

if __name__ == "__main__":
    main()
