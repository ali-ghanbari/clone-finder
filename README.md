# Automatic Goal Clone Detection in Rocq

This repository contains the source code of `clone-finder`.
This project depends on [CoqPyt](https://github.com/sr-lab/coqpyt), which must be installed before usage.

## Installation and usage instructions
To install and use `clone-finder`, please follow these instructions:
* Install [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) and create a virtual environment with Python 3.10.

```shell
conda create -n clone_finder python=3.10
activate clone_finder
```

* Clone CoqPyt and navigate to its directory to install the framework and its dependencies.

```shell
git clone https://github.com/sr-lab/coqpyt.git
cd coqpyt
pip install -r requirements.txt
python -m pip install -e .
```

* Now `clone-finder` is ready to use! Navigate to `clone-finder` source directory and run the tool following this tempelate.

```shell
cd ..
git clone https://github.com/ali-ghanbari/clone-finder.git
cd clone-finder
python main.py -b /path/to/your/Coq/project -p /physical/path/to/your/theories -l logicalPathForYourTheories -m Q/R
```
