import os

num_threads = '1'
# os.environ["MKL_NUM_THREADS"] = num_threads
# os.environ["NUMEXPR_NUM_THREADS"] = num_threads
# os.environ["OMP_NUM_THREADS"] = num_threads
# os.environ['OPENBLAS_NUM_THREADS'] = num_threads
# os.environ['VECLIB_MAXIMUM_THREADS'] = num_threads

import numpy as np
import igl
import scipy as sp
import datetime
import time
import solve_functions_limited


ITERATIVE_SOLVERS = (sp.sparse.linalg.bicg,
                     sp.sparse.linalg.bicgstab,
                     sp.sparse.linalg.cg,
                     sp.sparse.linalg.gmres,
                     # sp.sparse.linalg.lgmres,
                     sp.sparse.linalg.minres,
                     sp.sparse.linalg.qmr
                     # sp.sparse.linalg.gcrotmk
                     )

A, b, meshf, uk2, mesht = solve_functions_limited.laplace_setup("meshes/octopus.mesh__sf.obj",
                                                        [-5, 20])
A_f, factorized_A, b_f, meshf_f, uk2_f, \
mesht_f = solve_functions_limited.laplace_setup_factorized_back_substitution("meshes/octopus.mesh__sf.obj",
                                                                [-5, 20])
time_lim = 3600
residual_lim = 5
max_iterations = None
tol = 10**-5

direct_max_iter = None
direct_tol = None

for solve_fx in ITERATIVE_SOLVERS:
    solve_functions_limited.general_iterative_tracker(A, b, time_lim,
                                              solve_fx, tol, max_iterations,
                                              residual_lim,
                                              meshf, uk2, mesht)
solve_functions_limited.spsolve_tracker(A, b, time_lim,
                                sp.sparse.linalg.spsolve,
                                direct_tol, direct_max_iter,
                                residual_lim,
                                meshf, uk2, mesht)

solve_functions_limited.factorized_tracker(A, b, time_lim,
                                   sp.sparse.linalg.factorized,
                                   direct_tol, direct_max_iter,
                                   residual_lim,
                                   meshf, uk2, mesht)


solve_functions_limited.factorized_tracker_back_substitution(A_f, factorized_A, b_f, time_lim,
                                           sp.sparse.linalg.factorized,
                                           direct_tol, direct_max_iter,
                                           residual_lim,
                                           meshf_f, uk2_f, mesht)


