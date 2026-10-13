"""Finite-field point counts, zeta functions and a toy elliptic curve."""
from sympy import symbols, factor


def count_elliptic_fp(p,a,b):
    """Points on smooth y²=x³+ax+b over F_p (odd prime p)."""
    if p<=2: raise ValueError('Odd characteristic required')
    squares={y*y%p for y in range(p)}
    return 1+sum(sum(y*y%p == (x**3+a*x+b)%p for y in range(p)) for x in range(p))


def nonsquare_mod_p(p):
    squares={x*x%p for x in range(p)}
    return next(x for x in range(2,p) if x not in squares)


def count_elliptic_fp2(p,a,b):
    """Count curve points in F_{p²}=F_p[u]/(u²-d) for d nonsquare."""
    d=nonsquare_mod_p(p)
    elements=[(v,w) for v in range(p) for w in range(p)]
    def plus(x,y):return ((x[0]+y[0])%p,(x[1]+y[1])%p)
    def mul(x,y):return ((x[0]*y[0]+d*x[1]*y[1])%p,(x[0]*y[1]+x[1]*y[0])%p)
    sq={mul(y,y):0 for y in elements}
    for y in elements: sq[mul(y,y)]+=1
    return 1 + sum(sq.get(plus(plus(mul(mul(x,x),x),mul((a%p,0),x)),(b%p,0)),0) for x in elements)


def frobenius_trace(p,N1):
    return p+1-N1


def elliptic_extension_counts(p,trace,count):
    """Use Frobenius charpoly T²-aT+p for predicted #E(F_{p^n})."""
    if count<=0: return []
    a=frobenius_trace(p,trace)
    s0,s1=2,a
    counts=[]
    for n in range(1,count+1):
        if n==1: s=s1
        else:
            s0,s1=s1,a*s1-p*s0
            s=s1
        counts.append(p**n+1-s)
    return counts


def elliptic_zeta(p,N1):
    T=symbols('T')
    a=frobenius_trace(p,N1)
    return (1-a*T+p*T**2)/((1-T)*(1-p*T))
