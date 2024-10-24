from math import comb
import numpy as np

AAs = ['A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']

def get_OAAC(seq, k=3, AAs=AAs, normalize=True):
  """
  For k=1 computes the AAC features
  """
  AA_vals = dict(zip(AAs, list(np.arange(len(AAs))))) # mapping AA to array indices
  # kmers = [''.join(c) for c in product(('').join(np.array(AAs)), repeat=k)]
  feat_list = [np.zeros((len(AAs),)*(i+1)) for i in range(k)] # list of arrays for k-OAAC
  for AA in seq:
    if AA in AAs:
      for i in range(k-1, 0, -1):
        I = [slice(None)]*(i+1)
        I[i] = AA_vals[AA]
        feat_list[i][tuple(I)] += feat_list[i-1]
      feat_list[0][AA_vals[AA]] += 1 
  if normalize and feat_list[-1].sum()>0:
    return feat_list[-1].flatten()/feat_list[-1].sum()
  return feat_list[-1].flatten()

#################################################################################################################################################  
# LCS code
'''
Source: https://www.geeksforgeeks.org/printing-longest-common-subsequence/
by Shivam Tiwari
'''

from typing import Dict, Tuple

# Utility function to reverse a string, we need it because our top-down approach
# return a reversed solution
def reverse(s: str) -> str:
  ans = list(s)
  u, v = 0, len(ans) - 1
  while u < v:
    ans[u], ans[v] = ans[v], ans[u] #swap operation
    u += 1
    v -= 1
  return "".join(ans)

# Utility function that compares two strings and return the longer in size.
def max_str(a: str, b: str) -> str:
  return a if len(a) > len(b) else b

# Recursive function that takes two strings as input, and returns the LCS of them
def LCS_core(a: str, b: str, dp, vs) -> str:
  # Base case
  if not a or not b:
    return ""
  # dp index to access the dp structure
  dp_i = (a, b)

  # if visited return solution from memory
  if dp_i in vs:
    return dp[dp_i]
  else:
    vs[dp_i] = 1

  # if the last two character match
  if a[-1] == b[-1]:
    ans = a[-1] + LCS_core(a[:-1], b[:-1], dp, vs)
    dp[dp_i] = ans
    return ans

  # Return longest string
  ans = max_str(LCS_core(a[:-1], b, dp, vs), LCS_core(a, b[:-1], dp, vs))
  dp[dp_i] = ans
  return ans

# Final wrapper function to call the recursive function and reverse the result
def LCS(a: str, b: str) -> str:
  # Initialize an empty dictionary to store the solutions of subproblems
  dp: Dict[Tuple[str, str], str] = {}

  # Initialize an empty dictionary to keep track of visited subproblems
  vs: Dict[Tuple[str, str], int] = {}
  return reverse(LCS_core(a, b, dp, vs))
