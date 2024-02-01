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
def solver(a, b):
    udd_1 = sp.sparse.linalg.spsolve(a, b)
    udd_2 = sp.sparse.linalg.cg(a, b)
    udd_3 = sp.sparse.linalg.bicg(a, b)
    udd_4 = sp.sparse.linalg.bicgstab(a, b)
    udd_5 = sp.sparse.linalg.cgs(a, b)
    udd_6 = sp.sparse.linalg.gmres(a, b)
    udd_7 = sp.sparse.linalg.lgmres(a, b)
    udd_8 = sp.sparse.linalg.minres(a, b)
    udd_9 = sp.sparse.linalg.qmr(a, b)
    udd_10 = sp.sparse.linalg.gcrotmk(a, b)
    udd_11 = sp.sparse.linalg.tfqmr(a, b)

    return [udd_1, udd_2, udd_3, udd_4, udd_5, udd_6, udd_7, udd_8, udd_9,
            udd_10, udd_11]


print(solver(Ldd, rhs))
