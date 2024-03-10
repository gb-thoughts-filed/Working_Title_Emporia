# import polyscope as ps
import numpy as np
import igl
import scipy as sp
from datetime import datetime
import time
import cvxopt as cvx
from cvxopt import umfpack
# import matplotlib.pyplot as plt
v, _, _, f, _, _ = igl.read_obj("../octopus.mesh__sf.obj")
# ps.init()
# ps.register_surface_mesh("octopus", v, f)
# ps.show()

L = igl.cotmatrix(v, f)
