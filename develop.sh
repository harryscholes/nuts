conda create -n nuts python=3 jupyter nb_conda
source activate nuts
export PYTHONPATH=$PYTHONPATH:$PWD
pip install -r requirements.txt
