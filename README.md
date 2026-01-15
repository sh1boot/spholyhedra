# Spholyhedra.py

Generates STL for some regular polyhedra in their 'squircle' forms -- where the
edges are replaced with a smooth transitions in a generalisation on the
squircle function:

```math
|x|^a+|y|^a=1^a
```

Where $a$ is typically 3 or 4, and can be higher to be more squarish and lower
to be more circleish.

## setup

Needs `sdlfab` to be installed.  Like, with `pip install sdflab` or something like that.

## usage
```sh
python ./spholyhedra.py \
        [--shape={tetrahedron,cube,hexahedron,octahedron,dodecahedron,icosahedron}] \
        [--exponent=EXPONENT] \
        [--step=STEP] \
        [--output=OUTPUT]
```

This should generate an STL file with an approximate inradius of 10mm (or 10
STL units, or whatever), named `OUTPUT`.

`SHAPE` is your choice of solid.

`EXPONENT` needs to be something like 4 for a cube or tetrahedron, but a bit
bigger for shapes with more faces.  Maybe 16 for an icosahedron.

`STEP` decides the granularity of the mesh, and consequently the size of the
output file.  Smaller steps for more resolution.  1 is very coarse and 0.1 is a
big file.
