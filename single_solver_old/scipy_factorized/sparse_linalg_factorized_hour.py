# import polyscope as ps
import numpy as np
import igl
import scipy as sp
from datetime import datetime
import time

# import matplotlib.pyplot as plt
v, _, _, f, _, _ = igl.read_obj("octopus.mesh__sf.obj")
# ps.init()
# ps.register_surface_mesh("octopus", v, f)
# ps.show()

L = -igl.cotmatrix(v, f)
# print(L)


# plt.spy(L)
eps = 1e-12
i1 = np.where(v[:, 1] == v[:, 1].max())[0]  # top of octopus, indices known
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

def scipy_sparse_linalg_factorized(Ldd, rhs, timer):
    counter = 0
    title = datetime.today()
    time_file = open(f"sparse_linalg_factorized{title: %B%d%Y}.txt", "a")
    start_time = datetime.now()
    t1 = time.time()

    while time.time() - t1 < timer:
        solve = sp.sparse.linalg.factorized(Ldd)
        udd = solve(rhs)
        counter += 1

    end_time = datetime.now()

    counter2 = 0
    norms = []

    while counter2 < 5:
        solve = sp.sparse.linalg.factorized(Ldd)
        udd = solve(rhs)
        resid_norm = np.linalg.norm(Ldd@udd - rhs)
        norms.append(resid_norm)
        counter2 += 1
    avg_resid_norm = np.average(norms)
    time_file.write(f" \n {start_time}, {counter}, {end_time}, {avg_resid_norm}")

scipy_sparse_linalg_factorized(Ldd, rhs, 3600)
