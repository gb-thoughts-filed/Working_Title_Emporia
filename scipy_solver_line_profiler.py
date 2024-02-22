# import polyscope as ps
from line_profiler import profile
import numpy as np
import igl
import scipy as sp
from datetime import datetime
import time
import timeit
# import matplotlib.pyplot as plt
v, _, _, f, _, _ = igl.read_obj("octopus.mesh__sf.obj")
# ps.init()
# ps.register_surface_mesh("octopus", v, f)
# ps.show()

L = igl.cotmatrix(v, f)
# print(L)


# plt.spy(L)
eps = 1e-12
i1 = np.where(v[:, 1] == v[:, 1].max())[0] # top of octopus, indices known
i2 = np.where(v[:, 0] == v[:, 0].min())[0]

k = np.concatenate([i1, i2])

n = v.shape[0]
d = np.setdiff1d(np.arange(n), k)

Ldd = L[d, :][:, d]
Ldk = L[d, :][:, k]


# assemble uk=2 vector (u[k])
u_k = np.array([-5, 20])
# solve Ldd * udd = uk

rhs = -Ldk @ u_k

#print and save starting date/time to disk
#make a time loop that calls the next line for a whole hour or a whole day
#counter saved after each time the function is called
#print and save ending date time
#email stuff


@profile
def solvers_tol(a, b, solver):
    udd = solver(a, b, tol=10**-7)
    return udd

@profile
def solver_minres(a, b):
    udd = sp.sparse.linalg.minres(a, b, tol=10**-10)
    return udd

@profile
def solver_factorized(a, b):
    solve = sp.sparse.linalg.factorized(a)
    udd = solve(b)
    return udd

iterative_solver_list = [sp.sparse.linalg.bicgstab, sp.sparse.linalg.bicg,
               sp.sparse.linalg.cg,
               sp.sparse.linalg.gcrotmk, sp.sparse.linalg.gmres,
               sp.sparse.linalg.lgmres,
               sp.sparse.linalg.qmr]
norms = []
for i in iterative_solver_list:
    xk = solvers_tol(Ldd, rhs, i)
    norm = np.linalg.norm(Ldd@xk[0] - rhs)
    norms.append(norm)

udd_minres = solver_minres(Ldd, rhs)
udd_factorized = solver_factorized(Ldd, rhs)
udd_spsolve = sp.sparse.linalg.spsolve(Ldd, rhs)

norms.append(np.linalg.norm(Ldd @ udd_minres[0] - rhs))
norms.append(np.linalg.norm(Ldd @ udd_factorized - rhs))
norms.append(np.linalg.norm(Ldd @ udd_spsolve - rhs))
print(norms)

'''
xk = solvers_tol(Ldd, rhs)

print(np.linalg.norm(Ldd@xk[0] - rhs))
print(np.linalg.norm(Ldd@xk[0] - rhs) <= 10**-5)
print(xk)
'''
