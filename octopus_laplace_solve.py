import numpy as np
import igl
import scipy as sp
from datetime import datetime
import time
#import cvxopt as cvx
#from cvxopt import umfpack
#from scipy_spsolve import sparse_linalg_spsolve_hour
from scipy_tfqmr import scipy_sparse_linalg_tfqmr_hour
from scipy_factorized import sparse_linalg_factorized_hour
from scipy_bicgstab import scipy_sparse_linalg_bicgstab_hour
from scipy_biconjugate_gradient_iteration import scipy_bicg_hour
from scipy_cg import sparse_linalg_cg_hour
from scipy_gcrotmk import scipy_sparse_linalg_gcrotmk_hour
from scipy_gmres import scipy_sparse_linalg_gmres_hour
from scipy_lgmres import scipy_sparse_linalg_lgmres_hour
from scipy_minres import scipy_sparse_linalg_minres_hour
from scipy_qmr import scipy_sparse_linalg_qmr_hour
from scipy_cgs import scipy_sparse_linalg_cgs_hour

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
#d_Ldd = Ldd.tocoo()
#s_Ldd = cvx.spmatrix(d_Ldd.data, d_Ldd.row, d_Ldd.col)
Ldk = L[d, :][:, k]


# assemble uk=2 vector (u[k])
u_k = np.array([-5, 20])
# solve Ldd * udd = uk
rhs = -Ldk @ u_k
#rhs_cvx = cvx.matrix(rhs)

#sparse_linalg_spsolve_hour.sparse_linalg_spsolve(Ldd, rhs, 3600)

#time.sleep(600)

#scipy_sparse_linalg_tfqmr_hour.sparse_linalg_tfqmr(Ldd, rhs, 3600)

#time.sleep(600)

#sparse_linalg_factorized_hour.scipy_sparse_linalg_factorized(Ldd, rhs, 3600)

#time.sleep(600)

#scipy_sparse_linalg_bicgstab_hour.sparse_linalg_bicgstab(Ldd, rhs, 3600)

#time.sleep(600)

#scipy_bicg_hour.scipy_sparse_linalg_bicg(Ldd, rhs, 3600)

#time.sleep(600)

sparse_linalg_cg_hour.scipy_sparse_linalg_cg(Ldd, rhs, 3600)

time.sleep(600)

#scipy_sparse_linalg_gcrotmk_hour.sparse_linalg_gcrotmk(Ldd, rhs, 3600)

#time.sleep(600)

scipy_sparse_linalg_gmres_hour.sparse_linalg_gmres(Ldd, rhs, 3600)

time.sleep(600)

scipy_sparse_linalg_lgmres_hour.sparse_linalg_lgmres(Ldd, rhs, 3600)

time.sleep(600)

scipy_sparse_linalg_minres_hour.sparse_linalg_minres(Ldd, rhs, 3600)

time.sleep(600)

#scipy_sparse_linalg_qmr_hour.sparse_linalg_qmr(Ldd, rhs, 3600)

#time.sleep(600)

#scipy_sparse_linalg_cgs_hour.sparse_linalg_cgs(Ldd, rhs, 3600)





