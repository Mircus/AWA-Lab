"""Nodal dual graphs and genus conservation; symbolic singularity checks."""
import sympy as sp
import networkx as nx


def arithmetic_genus_dual_graph(vertex_genera,edges):
    """Connected nodal curve: p_a=sum genus(normalized components)+b_1(dual graph).

    Supports loop edges and multiple edges. vertices are indices 0...len-1.
    """
    g=nx.MultiGraph()
    g.add_nodes_from(range(len(vertex_genera)))
    g.add_edges_from(edges)
    if not nx.is_connected(g):
        raise ValueError('Curve should be connected')
    b1=g.number_of_edges()-g.number_of_nodes()+1
    return {'arithmetic_genus':sum(vertex_genera)+b1,'graph_betti_1':b1,'graph':g}


def discriminant_legendre():
    """Discriminant of x(x-1)(x-t) as polynomial in x."""
    x,t=sp.symbols('x t')
    return sp.factor(sp.discriminant(x*(x-1)*(x-t),x))


def nodal_parameterization():
    """Rational parametrization of y^2=x^2(x-1), over C."""
    u=sp.symbols('u'); x=u**2+1; y=u*(u**2+1)
    return x,y,sp.simplify(y**2-x**2*(x-1))
