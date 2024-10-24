"""
Code for SVEA algorithm based on
Tripathi, S.; Hemachandra, N.; and Trivedi, P. 2020. Interpretable feature subset selection: A Shapley value based approach. In 2020 IEEE International Conference on Big Data
(Big Data), 5463–5472

Algorithm 1 in https://arxiv.org/pdf/2001.03956.pdf

A class weighted hinge loss function is used instead of the standard hinge loss

Gurobi installation is required for running the solver.
A Gurobi license may also be required.
"""

import cvxpy as cp
import numpy as np
import itertools
import math
from tqdm.auto import tqdm

# CS training error function for no features
def CS_tr_er_null(y, C):
  m = len(y)
  classes = list(set(y))
  y_train = y.copy()
  y_train[y==classes[0]] = 1.0
  y_train[y==classes[1]] = -1.0  

  Psi = cp.Variable(m, nonneg=True)
  b = cp.Variable()

  constraints=[cp.multiply(y_train,b)-1 + Psi >= 0]
  objective = cp.Minimize(cp.sum(cp.multiply(Psi, C)))
  prob = cp.Problem(objective, constraints)
  prob.solve(solver = cp.GUROBI, verbose=False)
  # print(Psi.value, prob.status)

  return prob.value/float(m)

def CS_SVEA(X,y, samPerm, return_SV=False, seed=None):
  # X,y training samples
  m,n = X.shape
  Sh = np.zeros(n)
  Sam_co_set = [()]
  
  # set labels to {-1,1}
  classes = list(set(y))
  y_train = y.copy().astype(float)
  y_train[y==classes[0]] = 1.0
  y_train[y==classes[1]] = -1.0

  # set class-balanced loss weights
  C = y.copy().astype(float)
  C[y==classes[0]] = float(m)/(2*(y==classes[0]).sum())
  C[y==classes[1]] = float(m)/(2*(y==classes[1]).sum())

  c = CS_tr_er_null(y, C) # tr_er for null set
  tr_ers = {():c} # dictionary of training errors
  vals = {():0} # dictionary of values
  rng = np.random.default_rng(seed)
  
  Psi = cp.Variable(m, nonneg=True)
  b = cp.Variable()
  feature_set = cp.Parameter(n, nonneg=True)  
  W = cp.Variable(n)
  constraints= [cp.multiply(y_train, X@cp.multiply(W,feature_set) + b)-1 + Psi >= 0]
  objective = cp.Minimize(cp.sum(cp.multiply(Psi, C)))
  prob = cp.Problem(objective, constraints)
  
  pbar = tqdm(range(samPerm))
  for s in pbar:
    pi = list(rng.permutation(n))
    for j in range(n):
      set_val = np.zeros(n)
      pred_j = pi[:pi.index(j)]
      if tuple(np.sort(pred_j)) not in Sam_co_set:
        set_val[pred_j] = 1
        feature_set.value = set_val
        # tr_ers[tuple(np.sort(pred_j))] = tr_er(X[:,pred_j],y)
        prob.solve(solver = cp.GUROBI, verbose=False)
        vals[tuple(np.sort(pred_j))] = c - prob.value/float(m)
        Sam_co_set.append(tuple(np.sort(pred_j)))

      if tuple(np.sort(pred_j+[j])) not in Sam_co_set:
        set_val[pred_j+[j]] = 1
        feature_set.value = set_val
        # tr_ers[tuple(np.sort(pred_j+[j]))] = tr_er(X[:,pred_j+[j]],y)
        prob.solve(solver = cp.GUROBI, verbose=False)
        vals[tuple(np.sort(pred_j+[j]))] = c - prob.value/float(m)
        Sam_co_set.append(tuple(np.sort(pred_j+[j])))

      Sh[j] += vals[tuple(np.sort(pred_j+[j]))] - vals[tuple(np.sort(pred_j))]
  pbar.close()
  if return_SV:
    return Sh/samPerm
  return (c/n) - Sh/samPerm