This file contains the instructions for reproducing the results of the paper with the title - 'Identifying key amino acid types that distinguish paralogous proteins using Shapley value-based feature subset selection'.

- the `computational_experiments.ipynb` file contains the main code for the computational experiments.
- the `datasets` folder contains the datasets used in the experiments.
- the `heteromer_structure_fss_analysis.ipynb` file contains the code for counting the FSS amino acids present at the inter-chain contact points of the heteromers - tubulin and histone.
- the remaining `*.py` files contain utility functions called in the main code.

 # installation requirements
- It is recomended to create a conda environment with the following:
  - `Python 3.9.19`
  - the necessary python packages can be installed from the `requirements.txt` file using,
    - `pip install -r requirements.txt`
  - `Jupyterlab` for running `computational_experiments.ipynb` can be installed using,
    - `pip install jupyterlab==4.0.5`
  - `Gurobi 11.0.3` can be installed with a [free Academic license](https://support.gurobi.com/hc/en-us/articles/360040541251) using `conda install -c gurobi gurobi=11.0.3` as detailed in: <https://support.gurobi.com/hc/en-us/articles/360044290292-How-do-I-install-Gurobi-for-Python->
  - ClustalO for creating mutliple sequence alignments can be installed using
    - `conda install -c bioconda clustalo=1.2.3`
    