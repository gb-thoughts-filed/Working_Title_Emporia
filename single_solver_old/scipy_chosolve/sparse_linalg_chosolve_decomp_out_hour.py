# import polyscope as ps
import numpy as np
import igl
import scipy as sp
from datetime import datetime
import time
import cvxopt as cvx
# import matplotlib.pyplot as plt
v, _, _, f, _, _ = igl.read_obj("../../octopus.mesh__sf.obj")
# ps.init()
# ps.register_surface_mesh("octopus", v, f)
# ps.show()

L = igl.cotmatrix(v, f)
# print(L)


# plt.spy(L)
eps = 1e-12 #
i1 = np.where(v[:, 1] == v[:, 1].max())[0] # top of octopus, indices known
i2 = np.where(v[:, 0] == v[:, 0].min())[0]

k = np.concatenate([i1, i2])

n = v.shape[0]
d = np.setdiff1d(np.arange(n), k)

Ldd = L[d, :][:, d]
a_Ldd = Ldd.toarray()
Ldk = L[d, :][:, k]


# assemble uk=2 vector (u[k])
u_k = np.array([-5, 20])
# solve Ldd * udd = uk

rhs = -Ldk @ u_k



def sparse_linalg_chosolve_decomp_out(a_Ldd, rhs):
    cho_Ldd, u_or_l = sp.linalg.cho_factor(a_Ldd)
    counter = 0
    title = datetime.today()
    time_file = open(f"linalg_cho_solve_test{title: %B%d%Y}.txt", "a")
    start_time = datetime.now()
    t1 = time.time()

    while time.time() - t1 < 5:
        udd = sp.linalg.cho_solve(cho_Ldd, rhs)
        counter += 1

    end_time = datetime.now()

    counter2 = 0
    norms = []

    while counter2 < 100:
        udd = sp.sparse.linalg.spsolve(cho_Ldd, rhs)
        resid_norm = cho_Ldd@udd - rhs
        norms.append(resid_norm)
        counter2 += 1
    avg_resid_norm = np.average(resid_norm)
    time_file.write(f" \n {start_time}, {counter}, {end_time}, {avg_resid_norm}")

sparse_linalg_chosolve_decomp_out(a_Ldd, rhs)



