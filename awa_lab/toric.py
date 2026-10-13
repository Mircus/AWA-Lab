"""Small affine semigroups, lattice exponent geometry and binomial relations."""
from itertools import product
from math import gcd
from functools import reduce
import sympy as sp


def generated_exponents(generators, max_coefficient=5):
    """Set of exponent vectors formed with nonnegative coefficients <= bound."""
    gens = [tuple(g) for g in generators]
    if not gens or len({len(g) for g in gens}) != 1:
        raise ValueError('Generators must have same dimension')
    dimension = len(gens[0]); result = set()
    for weights in product(range(max_coefficient+1),repeat=len(gens)):
        result.add(tuple(sum(weights[i]*gens[i][j] for i in range(len(gens))) for j in range(dimension)))
    return result


def small_integer_relations(generators, coeff_bound=3):
    """Primitive binomial exponent relations with bounded coefficients.

    Searches for v in Z^r satisfying A*v=0 and gcd(v_i)=1.
    Opposite vectors are identified. NOT a toric-ideal generating algorithm.
    """
    gens = [tuple(g) for g in generators]; r = len(gens)
    results = set()
    for v in product(range(-coeff_bound,coeff_bound+1),repeat=r):
        if not any(v) or reduce(gcd,(abs(x) for x in v)) != 1: continue
        if any(sum(v[i]*gens[i][j] for i in range(r)) != 0 for j in range(len(gens[0]))): continue
        for entry in v:
            if entry:
                if entry < 0: v = tuple(-u for u in v)
                break
        results.add(tuple(v))
    return sorted(results)


def cusp_gaps(limit=18):
    """Nonnegative degrees absent from the semigroup <2,3> up to limit."""
    return [i for i in range(limit+1) if (i,) not in generated_exponents([(2,),(3,)], limit)]


def coordinate_ring_relation():
    """The quadratic affine toric cone uv=w^2, via elimination."""
    u,v,w,s,t = sp.symbols('u v w s t')
    gb = sp.groebner([u-s**2,w-s*t,v-t**2],s,t,u,v,w,order='lex')
    eliminated = [f.as_expr() for f in gb.polys if not f.as_expr().has(s,t)]
    return [sp.factor(f) for f in eliminated]
