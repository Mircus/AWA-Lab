"""Reproduce assets/tropical_line.png using the min-plus convention."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(8.6,3.2))
r=np.linspace(0,2.9,150);neg=np.linspace(-2.3,0,150)
ax.plot(np.zeros_like(r),r,linewidth=3,label='X=0, Y≥0')
ax.plot(r,np.zeros_like(r),linewidth=3,label='Y=0, X≥0')
ax.plot(neg,neg,linewidth=3,label='X=Y≤0')
ax.set(xlim=(-2.8,3.2),ylim=(-2.8,3.2),xlabel='X',ylabel='Y',title='The tropical line: min(0, X, Y) is attained at least twice')
ax.axhline(0,alpha=.16);ax.axvline(0,alpha=.16);ax.set_aspect('equal');ax.legend(loc='lower right',fontsize=8)
fig.tight_layout(); fig.savefig(root/'assets'/'tropical_line.png',dpi=140)
print('Saved',root/'assets'/'tropical_line.png')
