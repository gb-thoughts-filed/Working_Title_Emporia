import numpy as np
import igl
import scipy as sp
import datetime
import time
import solve_functions
import psutil
import os


ITERATIVE_SOLVERS = (sp.sparse.linalg.bicg,
                     sp.sparse.linalg.bicgstab,
                     sp.sparse.linalg.cg,
                     sp.sparse.linalg.gmres,
                     # sp.sparse.linalg.lgmres,
                     sp.sparse.linalg.minres,
                     sp.sparse.linalg.qmr
                     # sp.sparse.linalg.gcrotmk
                     )

A, b, meshf, uk2, mesht = solve_functions.laplace_setup("meshes/octopus.mesh__sf.obj",
                                                        [-5, 20])

time_lim = 5
residual_lim = 5
max_iterations = None
tol = 10**-1

direct_max_iter = None
direct_tol = None

for solve_fx in ITERATIVE_SOLVERS:
    solve_functions.general_iterative_tracker(A, b, time_lim,
                                              solve_fx, tol, max_iterations,
                                              residual_lim,
                                              meshf, uk2, mesht)
solve_functions.spsolve_tracker(A, b, time_lim,
                                sp.sparse.linalg.spsolve,
                                direct_tol, direct_max_iter,
                                residual_lim,
                                meshf, uk2, mesht)

solve_functions.factorized_tracker(A, b, time_lim,
                                   sp.sparse.linalg.factorized,
                                   direct_tol, direct_max_iter,
                                   residual_lim,
                                   meshf, uk2, mesht)





