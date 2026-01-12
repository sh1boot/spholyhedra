import argparse
import math
from sdf import *
from sdf.d3 import sdf3, ORIGIN

def psum(*args, n=1):
    return pow(sum(map(lambda x: pow(x, n), args)), 1.0 / n)

# TODO: orient all of these consistently.

@sdf3
def sphube(radius=1, n=4, centre=ORIGIN):
    def f(p):
        p = abs(p - centre) / radius
        px, py, pz = p[:,0], p[:,1], p[:,2]
        return psum(px, py, pz, n=n) - 1.0
    return f

@sdf3
def sphoctahedron(radius=1, n=6, centre=ORIGIN):
    radius *= math.sqrt(3)
    def f(p):
        p = (p - centre) / radius
        px, py, pz = p[:,0], p[:,1], p[:,2]
        w = [px + py + pz,
             px + py - pz,
             px - py + pz,
             px - py - pz]
        return psum(*map(abs,w), n=n) - 1.0
    return f

@sdf3
def sphodecahedron(radius=1, n=9, centre=ORIGIN):
    dihedral = math.acos(math.sqrt(5) / -5)
    c = math.cos(dihedral)
    s = math.sin(dihedral)
    def f(p):
        p = (p - centre) / radius
        px, py, pz = p[:,0], p[:,1], p[:,2]
        w = [pz]
        for i in range(5):
            x = px * math.cos(math.tau * i / 5)
            y = py * math.sin(math.tau * i / 5)
            w.append(s * (x + y) + c * pz)
        return psum(*map(abs, w), n=n) - 1.0
    return f

@sdf3
def sphicosahedron(radius=1, n=9, centre=ORIGIN):
    # TODO: make this right.
    dihedral = math.acos(math.sqrt(5) / -3)
    top = math.acos(math.sqrt((5 - math.sqrt(5)) / 8))
    side = top + dihedral
    c0 = math.cos(top)
    s0 = math.sin(top)
    c1 = math.cos(side)
    s1 = math.sin(side)
    def f(p):
        p = (p - centre) / radius
        px, py, pz = p[:,0], p[:,1], p[:,2]
        w = []
        for i in range(5):
            x = px * math.cos(math.tau * i / 5)
            y = py * math.sin(math.tau * i / 5)
            w.append(c0 * (x + y) + s0 * pz)
            w.append(c1 * (x + y) + s1 * pz)
        return psum(*map(abs, w), n=n) - 1.0
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
    bounds = ((-17, -17, -17), (17, 17, 17))

    match args.shape.lower():
        case '6' | 'cube' | 'hexahedron':
            solid = sphube(radius, args.exponent)
        case '8' | 'octahedron':
            solid = sphoctahedron(radius, args.exponent)
        case '12' | 'dodecahedron':
            solid = sphodecahedron(radius, args.exponent)
        case '20' | 'icosahedron':
            solid = sphicosahedron(radius, args.exponent)
        case '_':
            exit(-1)

    solid.save(args.output, step=args.step, bounds=bounds)
    print(f"Saved to: {args.output}")

if __name__ == "__main__":
    main()
