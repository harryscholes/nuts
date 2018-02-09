# nuts [![Build Status](https://travis-ci.org/harryscholes/nuts.svg?branch=master)](https://travis-ci.org/harryscholes/nuts) [![Coverage Status](https://codecov.io/gh/harryscholes/nuts/branch/master/graph/badge.svg)](https://codecov.io/gh/harryscholes/nuts?branch=master)
Python package for calculating kernels on graphs.

## Requirements

[Anaconda](https://anaconda.org/)
 
## Installation

```bash
bash install.sh
```

## Quick start guide

Given a network `G`:
```python

import networkx as nx
from nuts import Kernel

G = nx.erdos_renyi_graph(10, 0.2, seed=1)
```

the commute time kernel can be calculated by:
```python
k = Kernel(G)
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

from nuts import load_from_hdf5
load_from_hdf5(filepath)
```

## Example workflow
```python
import networkx as nx
from nuts import Kernel, load_from_hdf5

G = nx.erdos_renyi_graph(10, 0.2, seed=1)

k = Kernel(G)
k.calculate("CT")

if not k.valid():
    k.make_valid()
    
k.normalize()
k.write("kernel.h5")

kernel, mapping = load_from_hdf5("kernel.h5")
```
    
