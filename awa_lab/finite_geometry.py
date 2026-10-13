"""Finite Grassmannians and q-analogues via reduced row echelon forms."""
from itertools import combinations, product, permutations
from math import prod
from sympy import Symbol, expand


def inversion_number(perm):
    return sum(perm[i] > perm[j] for i in range(len(perm)) for j in range(i+1,len(perm)))


def flag_poincare_polynomial(n):
    """Poincare polynomial sum_{w in S_n} q^{length(w)}."""
    q = Symbol('q')
    return expand(sum(q**inversion_number(w) for w in permutations(range(n))))


def gaussian_polynomial(n, k):
    """Gaussian binomial coefficient via polynomial recurrence."""
    if not 0 <= k <= n:
        raise ValueError('Require 0 <= k <= n')
    q = Symbol('q')
    dp = {(i,0): 1 for i in range(n+1)}
    for i in range(1,n+1):
        for j in range(1,i+1):
            dp[i,j] = 1 if j == i else dp[i-1,j] + q**(i-j)*dp[i-1,j-1]
    return expand(dp[n,k])


def rref_matrices(n,k,p):
    """Generate the unique RREF representative of every k-plane in F_p^n.

    p must be prime. No primality test is performed. Moderate n,k,p only.
    """
    if not 0 <= k <= n or p < 2:
        raise ValueError('Invalid parameters')
    for piv in combinations(range(n),k):
        free = [(i,j) for i in range(k) for j in range(piv[i]+1,n) if j not in piv]
        for values in product(range(p),repeat=len(free)):
            a = [[0]*n for _ in range(k)]
            for i,col in enumerate(piv): a[i][col] = 1
            for (i,j),v in zip(free,values): a[i][j] = v
            yield tuple(tuple(row) for row in a)


def grassmannian_count(n,k,q):
    """Number of k-dimensional subspaces of F_q^n, q a prime power."""
    if not 0 <= k <= n or q < 2:
        raise ValueError('Invalid parameters')
    return prod(q**(n-i)-1 for i in range(k)) // prod(q**(k-i)-1 for i in range(k)) if k else 1


def schubert_cell_dimensions(n,k):
    """Dimension of RREF Schubert cells; one entry per pivot pattern."""
    return {tuple(piv): sum(n-piv[i]-1 - sum(j>piv[i] for j in piv) for i in range(k))
            for piv in combinations(range(n),k)}
