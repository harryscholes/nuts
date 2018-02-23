# nuts [![Build Status](https://travis-ci.org/harryscholes/nuts.svg?branch=master)](https://travis-ci.org/harryscholes/nuts) [![Coverage Status](https://codecov.io/gh/harryscholes/nuts/branch/master/graph/badge.svg)](https://codecov.io/gh/harryscholes/nuts?branch=master)
Python package for calculating kernels on graphs.

## Requirements

[Anaconda](https://anaconda.org/)

## Installation
nuts can be installed locally or via a Docker container.

### Local
```bash
bash install.sh
```

### Docker container
```bash
docker run \
    -p 8888:8888 \
    -v $PWD:/home/mount_volume \
    -it \
    harryscholes/nuts:latest
```

To mount a different directory in the container, substitute `$PWD` with your directory's path. This allows the container to read and write to the host filesystem.

## Quick start guide

Given a network `G`:
```python

import networkx as nx
from nuts import Kernel

G = nx.erdos_renyi_graph(10, 0.2, seed=1)
```

the commute time kernel can be calculated by:
```python
k = Kernel()
k.graph(G)
k.calculate("CT")
```

The kernel matrix and a dictionary mapping graph nodes to matrix indices can be accessed by:
```python
k.kernel
k.mapping
```

The kernel can be checked for validity, made valid (if necessary) and normalized––using the matrix cosine––by
```python
k.valid()
k.make_valid()
k.normalize()
```

The kernel can be written to, and read from, HDF5 using:
```python
k.write(filepath, *args)

k = Kernel()
kernel, mapping = k.read(filepath)
```

## Example workflow
```python
import networkx as nx
from nuts import Kernel

G = nx.erdos_renyi_graph(10, 0.2, seed=1)

k = Kernel()
k.graph(G)
k.calculate("CT")

if not k.valid():
    k.make_valid()

k.normalize()
k.write("kernel.h5")

k = Kernel()
kernel, mapping = k.read("kernel.h5")
```
