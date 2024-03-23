# import polyscope as ps
import numpy as np
import igl
import scipy as sp
from datetime import datetime
import time

# import matplotlib.pyplot as plt
v, _, _, f, _, _ = igl.read_obj("../../octopus.mesh__sf.obj")
# ps.init()
# ps.register_surface_mesh("octopus", v, f)
# ps.show()

L = igl.cotmatrix(v, f)
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

counter = 0
title = datetime.today()
time_file = open(f"sparse_linalg_spsolve_fixed_iter{title: %B%d%Y}.txt", "a")
start_time = datetime.now()
t1 = time.time()
# print and save starting date/time to disk
# make a time loop that calls the next line for a whole hour or a whole day
# counter saved after each time the function is called
# print and save ending date time
# email stuff
while counter < 1000:
    udd = sp.sparse.linalg.spsolve(Ldd, rhs)
    counter += 1

end_time = datetime.now()

time_file.write(f" \n {start_time}, {counter}, {end_time}")
