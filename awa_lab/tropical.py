"""Tropical hypersurfaces and Newton polygons (min-plus convention)."""
from fractions import Fraction


def trop_polynomial(terms, point):
    """Min of valuation + <exponents,point>; return (min, minimizer indices)."""
    values = [val + sum(a*x for a,x in zip(exponent,point)) for exponent,val in terms]
    minimum = min(values)
    return minimum,tuple(i for i,v in enumerate(values) if v==minimum)


def lower_newton_hull(points):
    """Vertices on lower convex hull of distinct (exponent,valuation) data."""
    pts = sorted((int(i),Fraction(v)) for i,v in points)
    if len({p[0] for p in pts}) != len(pts):
        raise ValueError('Only one valuation per exponent')
    lower=[]
    for p in pts:
        while len(lower)>=2:
            a,b=lower[-2:]
            cross=(b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
            if cross <= 0: lower.pop()
            else: break
        lower.append(p)
    return lower


def root_valuation_prediction(points):
    """Predicted nonzero root valuations and multiplicities from Newton polygon.

    Assumes a complete non-Archimedean valued field and generic nonzero
    leading coefficients; slopes as usual, repeated by horizontal length.
    """
    hull=lower_newton_hull(points)
    answer=[]
    for left,right in zip(hull,hull[1:]):
        slope=(right[1]-left[1]) / (right[0]-left[0])
        answer += [-slope] * (right[0]-left[0])
    return answer


def min_plus_matmul(A,B):
    """Tropical (min,+) matrix product; np.inf allowed."""
    if not A or not B or len(A[0]) != len(B):
        raise ValueError('Matrix dimensions differ')
    return [[min(A[i][k]+B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
