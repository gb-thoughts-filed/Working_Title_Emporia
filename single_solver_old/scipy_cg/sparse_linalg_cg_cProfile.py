# import polyscope as ps
import numpy as np
import igl
import scipy as sp
from datetime import datetime
import time
import cProfile
# import matplotlib.pyplot as plt
v, _, _, f, _, _ = igl.read_obj("../../octopus.mesh__sf.obj")
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


def loop(initial_time, calc_Ldd, calc_rhs):
    counter = 0
    calc_udd = 0
    while time.time() - initial_time < 10:
        calc_udd = sp.sparse.linalg.cg(calc_Ldd, calc_rhs)
    counter += 1
    return calc_udd


counter = 'null'
title = datetime.today()
time_file = open(f"sparse_linalg_cg_cProfile {title: %B%d%Y}.txt", "a")
start_time = datetime.now()
t1 = time.time()
#print and save starting date/time to disk
#make a time loop that calls the next line for a whole hour or a whole day
#counter saved after each time the function is called
#print and save ending date time
#email stuff
cProfile.run('loop(t1, Ldd, rhs)')
udd = loop(t1, Ldd, rhs)
end_time = datetime.now()

time_file.write(f" \n {start_time}, {counter}, {end_time}")
