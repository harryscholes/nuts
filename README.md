# nuts [![Build Status](https://travis-ci.org/harryscholes/nuts.svg?branch=master)](https://travis-ci.org/harryscholes/nuts) [![Coverage Status](https://codecov.io/gh/harryscholes/nuts/branch/master/graph/badge.svg)](https://codecov.io/gh/harryscholes/nuts?branch=master)
Python package for calculating kernels on graphs


## Examples

```python

import networkx as nx
from nuts import Kernel

G = nx.erdos_renyi_graph(10, 0.2, seed=1)

k = Kernel(G)
```

To calculate the commute time kernel
```python
k.calculate("CT")
```

The kernel matrix and a dictionary mapping graph nodes to matrix indices can be accessed by
```python
k.kernel
k.mapping
```

The validity of the kernel can be checked by `k.valid()`. Invalid kernels can be made valid by `k.make_valid()`.

Kernels can be normalized using the cosine of the matrix by `k.normalize()`.

To save the kernels to disk and and reload them
```python

k.write(filepath, ...)

from nuts.io import load_from_hdf5
load_from_hdf5(filepath)
```
