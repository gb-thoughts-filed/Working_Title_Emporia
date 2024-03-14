import numpy as np
import igl
import scipy as sp
import datetime
import time
import solve_functions
from solve_functions import LaplaceEquationSetup


ITERATIVE_SOLVERS = {sp.sparse.linalg.bicg,
                     sp.sparse.linalg.bicgstab,
                     sp.sparse.linalg.cg,
                     sp.sparse.linalg.gmres,
                     # sp.sparse.linalg.lgmres,
                     sp.sparse.linalg.minres,
                     sp.sparse.linalg.qmr
                     # sp.sparse.linalg.gcrotmk
                     }

solver_system = LaplaceEquationSetup("meshes/octopus.mesh__sf.obj", [-5, 20])

#A, b, meshf, uk2, mesht = solve_functions.laplace_setup("meshes/octopus.mesh__sf.obj",
#                                                        [-5, 20])


class Solver:
    def __init__(self, system_of_linear_equations: LaplaceEquationSetup):
        self.time_lim = 3600
        self.residual_lim = 5
        self.system_of_linear_equations = system_of_linear_equations


class IterativeSolver(Solver):
    def __init__(self):
        super().__init__()
        self.max_iterations = None
        self.tol = 10**-7

    def solve(self, A, b):
        for solver in ITERATIVE_SOLVERS:
            solve_functions.general_iterative_tracker(
                A,
                b,
                self.time_lim,
                solver,
                self.tol,
                self.max_iterations,
                self.residual_lim,
                self.system_of_linear_equations.mesh_filename,
                self.system_of_linear_equations.uk2_vector,
                self.system_of_linear_equations.mesh_calltime
            )


class DirectSolver(Solver):
    def __init__(self):
        super().__init__()
        self.direct_max_iter = None
        self.direct_tol = None

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





