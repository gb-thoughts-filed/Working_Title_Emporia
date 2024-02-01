import cvxpy as cp
import polyscope as ps
import numpy as np
import igl
import scipy as sp
# import matplotlib.pyplot as plt
v, _, _, f, _, _ = igl.read_obj("octopus.mesh__sf.obj")
# ps.init()
# ps.register_surface_mesh("octopus", v, f)
# ps.show()

L = igl.cotmatrix(v, f)
# print(L)


# plt.spy(L)
eps = 1e-12
i1 = np.where(v[:, 1] == v[:, 1].max())[0]  # top of octopus, indices known
i2 = np.where(v[:, 0] == v[:, 0].min())[0]
print("column one min", i1)
#i1 = np.where(v[:, 1] == v[:, 1].max())[0]
#print("column one max", i1)
i2 = np.where(v[:, 2] == v[:, 2].max())[0]


k = np.concatenate([i1, i2])

n = v.shape[0]
d = np.setdiff1d(np.arange(n), k)

Ldd = L[d, :][:, d]
Ldk = L[d, :][:, k]


# assemble uk=2 vector (u[k])
u_k = np.array([-5, 20])
# solve Ldd * udd = uk
udd = sp.sparse.linalg.spsolve(Ldd, -Ldk @ u_k)
# reconstruct u from udd and uk

print("residual", Ldd*udd - -Ldk @ u_k)
print("average residual", np.average(Ldd*udd - -Ldk @ u_k))

u = np.zeros((n))
u[k] = u_k
u[d] = udd

# visualize the resulting u on the octopus mesh using polyscope.
ps.init()
mesh = ps.register_surface_mesh("octopus", v, f)
mesh.add_scalar_quantity("u", u)
ps.show()
# also make a point cloud at v[k, :] to see where are the two constraint points.
