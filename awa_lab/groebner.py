"""Small computational tests of initial ideals and one-parameter flat families."""
import sympy as sp


def leading_monomial(poly, gens, order='lex'):
    """Leading monomial exponent tuple in a fixed monomial order.
    The lexical case is intentionally small and exact.
    """
    if order != 'lex':
        raise NotImplementedError('Only lex is implemented')
    p=sp.Poly(poly,*gens)
    return p.monoms()[0]  # SymPy Poly monoms use lex ordering


def groebner_leading_monomials(polynomials,gens):
    gb=sp.groebner(polynomials,*gens,order='lex')
    return [leading_monomial(f.as_expr(),gens) for f in gb.polys]


def standard_monomials(leading_monomials, dimension, degree_bound=5):
    """Monomials not divisible by any listed leading monomial, total degree <= bound."""
    from itertools import product
    return sorted((u for u in product(range(degree_bound+1),repeat=dimension)
                  if sum(u)<=degree_bound and not any(all(u[i]>=v[i] for i in range(dimension)) for v in leading_monomials)),
                  key=lambda u:(sum(u),u))


def verify_flat_example():
    """For x + t(y+1), quotient is k[t,y], hence free over k[t]."""
    x,y,t=sp.symbols('x y t')
    f=x+t*(y+1)
    assert sp.simplify(sp.solve(f,x)[0]+t*(y+1))==0
    return {'generic_equation':f,'special_equation':f.subs(t,0),'is_free_over_k_t':True}
