"""Exact, deterministic invariants underlying the six labs."""
import math
import pytest
import sympy as sp
from awa_lab.finite_geometry import (gaussian_polynomial,grassmannian_count,rref_matrices,flag_poincare_polynomial,schubert_cell_dimensions)
from awa_lab.toric import generated_exponents,small_integer_relations,cusp_gaps,coordinate_ring_relation
from awa_lab.tropical import lower_newton_hull,root_valuation_prediction,trop_polynomial,min_plus_matmul
from awa_lab.groebner import groebner_leading_monomials,standard_monomials,verify_flat_example
from awa_lab.stable_curves import arithmetic_genus_dual_graph,discriminant_legendre,nodal_parameterization
from awa_lab.zeta import (count_elliptic_fp,count_elliptic_fp2,elliptic_extension_counts,elliptic_zeta)

q=sp.Symbol('q'); x,y=sp.symbols('x y')
@pytest.mark.parametrize('n,k,p', [(3,1,2),(4,2,2),(3,2,3),(4,0,2)])
def test_grassmannian_rref_matches_gaussian(n,k,p):
    assert len(list(rref_matrices(n,k,p)))==grassmannian_count(n,k,p)
    assert gaussian_polynomial(n,k).subs(q,p)==grassmannian_count(n,k,p)

@pytest.mark.parametrize('n,k',[(2,1),(4,2),(5,3)])
def test_q_at_one(n,k):
    assert gaussian_polynomial(n,k).subs(q,1)==math.comb(n,k)
    assert sp.expand(sum(q**d for d in schubert_cell_dimensions(n,k).values())-gaussian_polynomial(n,k))==0

def test_flag_bruhat():
    assert flag_poincare_polynomial(4).subs(q,1)==24
    assert sp.expand(flag_poincare_polynomial(4)-(q+1)*(q**2+q+1)*(q**3+q**2+q+1))==0

def test_toric_relation_and_cusp():
    assert (1,-2,1) in small_integer_relations([(2,0),(1,1),(0,2)],2)
    u,v,w=sp.symbols('u v w')
    assert [sp.factor(f) for f in coordinate_ring_relation()]==[u*v-w**2]
    assert cusp_gaps(12)==[1]
    assert (1,1) not in generated_exponents([(2,0),(0,2)],max_coefficient=3)

def test_newton_roots():
    assert root_valuation_prediction([(0,4),(1,2),(3,0)])==[2,1,1]
    assert lower_newton_hull([(0,2),(1,1),(2,0)])==[(0,2),(2,0)]

def test_min_plus():
    t=[((0,0),0),((1,0),0),((0,1),0)]
    assert len(trop_polynomial(t,(0,2))[1])==2
    assert len(trop_polynomial(t,(2,3))[1])==1
    inf=float('inf')
    assert min_plus_matmul([[0,3],[inf,0]],[[0,2],[5,0]])==[[0,2],[5,0]]

def test_groebner_completion():
    assert groebner_leading_monomials([x+y,x-y],(x,y))==[(1,0),(0,1)]
    assert standard_monomials([(1,0),(0,1)],2,5)==[(0,0)]
    assert verify_flat_example()['is_free_over_k_t']

def test_nodal_genus_and_discriminant():
    t=sp.Symbol('t')
    assert sp.factor(discriminant_legendre())==t**2*(t-1)**2
    assert nodal_parameterization()[2]==0
    assert arithmetic_genus_dual_graph([0],[(0,0)])['arithmetic_genus']==1
    assert arithmetic_genus_dual_graph([0,0],[(0,1),(0,1)])['graph_betti_1']==1
    assert arithmetic_genus_dual_graph([0,0,0],[(0,1),(1,2)])['graph_betti_1']==0
    with pytest.raises(ValueError): arithmetic_genus_dual_graph([0,0],[])

def test_frobenius_count():
    assert count_elliptic_fp(5,1,1)==9
    assert count_elliptic_fp2(5,1,1)==27
    assert elliptic_extension_counts(5,9,3)==[9,27,108]
    T=sp.Symbol('T')
    assert sp.factor(elliptic_zeta(5,9)-(1+3*T+5*T*T)/((1-T)*(1-5*T)))==0
