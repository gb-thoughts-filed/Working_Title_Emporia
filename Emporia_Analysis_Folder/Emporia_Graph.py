import numpy as np
import matplotlib.pyplot as plt

'''
RESULT_FILE_HEADERS = ("python file name",
                       "solver name",
                       "start time",
                       "end time",
                       "time difference (s)",
                       "avg power (W)",
                       "avg power - base (W)",
                       "total solves",
                       "avg resid norm",
                       "seconds in single loop",
                       "energy one solve (J)",
                       "tolerance",
                       "max iterations",
                       "residual count limit",
                       "machine information",
                       "mesh filename",
                       "uk vector",
                       "cpu percentage")
'''

_, name, _, _, time_diff, avg_pwr, avg_pwr_base, total_solves, avg_resid_norm, \
time_single_loop, energy_one_solve, _, _, _, _, _, _, _ = \
    np.loadtxt("tolerance_testing_20240314/Emporia_Results_Extended_20240310201806.csv", skiprows=1, delimiter=",", dtype=str,
               unpack=True)

_, name1, _, _, time_diff1, avg_pwr1, avg_pwr_base1, total_solves1, avg_resid_norm1, \
time_single_loop1, energy_one_solve1, _, _, _, _ = \
    np.loadtxt("tolerance_testing_20240510/Emporia_Results_Extended_20240505172928.csv", skiprows=1, delimiter=",", dtype=str,
               unpack=True)

energy_one_solve = [float(i) for i in energy_one_solve]
# print(energy_one_solve)
time_single_loop = [float(i) for i in time_single_loop]

energy_one_solve1 = [float(i) for i in energy_one_solve1]
# print(energy_one_solve)
time_single_loop1 = [float(i) for i in time_single_loop1]


plt.scatter((time_single_loop), (energy_one_solve))
plt.scatter((time_single_loop1), (energy_one_solve1))
plt.title("Time v.s. Energy Plot")
plt.xlabel("Seconds Single Loop")
plt.ylabel("Energy Single Loop")
for (s, i, j) in zip(name, (time_single_loop), (energy_one_solve)):
    plt.text(i, j, f"{s}", fontsize=20)
for (l, m, n) in zip(name1, (time_single_loop1), (energy_one_solve1)):
    plt.text(m, n, f"{l}", fontsize=20)
plt.figure()

plt.show()
