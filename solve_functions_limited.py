import os

num_threads = '1'
os.environ["MKL_NUM_THREADS"] = num_threads
os.environ["NUMEXPR_NUM_THREADS"] = num_threads
os.environ["OMP_NUM_THREADS"] = num_threads
os.environ['OPENBLAS_NUM_THREADS'] = num_threads
os.environ['VECLIB_MAXIMUM_THREADS'] = num_threads

import numpy as np
import igl
import scipy as sp
import datetime
import time
import platform
import psutil

def laplace_setup(mesh, uk2_vector):

    v, _, _, f, _, _ = igl.read_obj(mesh)

    uk2_vector_name = str(uk2_vector)

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
    u_k = np.array(uk2_vector)
    # solve Ldd * udd = uk

    rhs = -Ldk @ u_k

    # Processing mesh file name.
    mesh_filename = mesh.replace("/", "_").replace(".", "_")

    # Processing mesh call time

    mesh_calltime = datetime.datetime.now()
    mesh_calltime = mesh_calltime.strftime("%Y%m%d%H%M%S")

    os.mkdir(f"{mesh_filename}_{mesh_calltime}")

    return Ldd, rhs, mesh_filename, uk2_vector_name, mesh_calltime

# A, b, meshf, uk2, mesh_t = laplace_setup("meshes/octopus.mesh__sf.obj", [-5, 20])

def general_iterative_tracker(Ldd, rhs, timer, solver,
                      tolerance, max_iter, resid_count_lim,
                              mesh_filename, uk2_vector, mesh_t):
    solver_name = f"{solver.__name__}"
    counter = 0
    title = datetime.datetime.today()
    time_file = open(f"{mesh_filename}_{mesh_t}/{solver_name}_{title:%B%d%Y}.txt", "a")
    start_time = datetime.datetime.now()
    t1 = time.time()

    while time.time() - t1 < timer:
        udd = solver(Ldd, rhs, tol=tolerance, maxiter=max_iter)
        counter += 1

    end_time = datetime.datetime.now()

    counter2 = 0
    norms = []

    while counter2 < resid_count_lim:
        udd = solver(Ldd, rhs, tol=tolerance, maxiter=max_iter)
        cpu_percent = psutil.cpu_percent()
        resid_norm = np.linalg.norm(Ldd@udd[0] - rhs)
        norms.append(resid_norm)
        counter2 += 1
    avg_resid_norm = np.average(norms)
    time_file.write(f" \n {start_time}, {counter}, "
                    f"{end_time}, {avg_resid_norm}, {solver_name}, "
                    f"{tolerance}, {max_iter}, {resid_count_lim}, "
                    f"{platform.uname()}, {mesh_filename}, {uk2_vector},"
                    f"{cpu_percent}")


def spsolve_tracker(Ldd, rhs, timer, solver,
                    tolerance, max_iter, resid_count_lim,
                    mesh_filename, uk2_vector, mesh_t):

    solver_name = f"{solver.__name__}"
    counter = 0
    title = datetime.datetime.today()
    time_file = open(f"{mesh_filename}_{mesh_t}/{solver_name}_{title:%B%d%Y}.txt", "a")
    start_time = datetime.datetime.now()
    t1 = time.time()

    while time.time() - t1 < timer:
        udd = solver(Ldd, rhs)
        counter += 1

    end_time = datetime.datetime.now()

    counter2 = 0
    norms = []

    while counter2 < resid_count_lim:
        udd = solver(Ldd, rhs)
        cpu_percent = psutil.cpu_percent()
        resid_norm = np.linalg.norm(Ldd@udd - rhs)
        norms.append(resid_norm)
        counter2 += 1
    avg_resid_norm = np.average(norms)
    time_file.write(f" \n {start_time}, {counter}, "
                    f"{end_time}, {avg_resid_norm}, {solver_name}, "
                    f"{tolerance}, {max_iter}, {resid_count_lim}, "
                    f"{platform.uname()}, {mesh_filename}, {uk2_vector}"
                    f"{cpu_percent}")

def factorized_tracker(Ldd, rhs, timer, solver,
                    tolerance, max_iter, resid_count_lim,
                       mesh_filename, uk2_vector, mesh_t):

    solver_name = f"{solver.__name__}"
    counter = 0
    title = datetime.datetime.today()
    time_file = open(f"{mesh_filename}_{mesh_t}/{solver_name}_{title:%B%d%Y}.txt", "a")
    start_time = datetime.datetime.now()
    t1 = time.time()

    while time.time() - t1 < timer:
        solve = solver(Ldd)
        udd = solve(rhs)
        counter += 1
        # to be considered two functions second called back substition,
        # lift solve = factorized(Ldd) to its own laplace setup function

    end_time = datetime.datetime.now()

    counter2 = 0
    norms = []

    while counter2 < resid_count_lim:
        solve = solver(Ldd)
        udd = solve(rhs)
        cpu_percent = psutil.cpu_percent()
        resid_norm = np.linalg.norm(Ldd@udd - rhs)
        norms.append(resid_norm)
        counter2 += 1
    avg_resid_norm = np.average(norms)
    time_file.write(f" \n {start_time}, {counter}, "
                    f"{end_time}, {avg_resid_norm}, {solver_name}, "
                    f"{tolerance}, {max_iter}, {resid_count_lim}, "
                    f"{platform.uname()}, {mesh_filename}, {uk2_vector}"
                    f"{cpu_percent}")
