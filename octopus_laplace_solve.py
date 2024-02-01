import numpy as np
import igl
import scipy as sp
from datetime import datetime
import time
import cvxopt as cvx
from sparse_linalg_chosolve_decomp_out_hour import sparse_linalg_chosolve_decomp_out_hour
# import matplotlib.pyplot as plt
v, _, _, f, _, _ = igl.read_obj("octopus.mesh__sf.obj")



# Set up Laplace system

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

sparse_linalg_chosolve_decomp_out_hour(Ldd, rhs, output_dir)
sparse_linalg_spsolve_hour((Ldd, rhs, output_dir)
# ... etc
