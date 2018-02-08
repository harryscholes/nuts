conda create -n nuts python=3 jupyter nb_conda
source activate nuts
pip install -e .
pip install -r requirements.txt
