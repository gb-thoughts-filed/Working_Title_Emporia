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

_, name_0314_8cores, _, _, time_diff_0314_8cores, avg_pwr_0314_8cores, \
 avg_pwr_base_0314_8cores, total_solves_0314_8cores, avg_resid_norm_0314_8cores, \
time_single_loop_0314_8cores, energy_one_solve_0314_8cores, _, _, _, _, _, _, _ = \
    np.loadtxt("tolerance_testing_20240314/Emporia_Results_Extended_20240311191802.csv", skiprows=1, delimiter=",", dtype=str,
               unpack=True)

_, name_0510_1core, _, _, time_diff1_0510_1core, \
 avg_pwr1_0510_1core, avg_pwr_base_0510_1core, total_solves_0510_1core, avg_resid_norm_0510_1core, \
time_single_loop_0510_1core, energy_one_solve_0510_1core, _, _, _, _ = \
    np.loadtxt("tolerance_testing_20240510/Emporia_Results_Extended_20240506222803.csv", skiprows=1, delimiter=",", dtype=str,
               unpack=True)

_, name_0514_8cores, _, _, time_diff1_0514_8cores, \
 avg_pwr1_0514_8cores, avg_pwr_base_0514_8cores, total_solves_0514_8cores, avg_resid_norm_0514_8cores, \
time_single_loop_0514_8cores, energy_one_solve_0514_8cores, _, _, _, _ = \
    np.loadtxt("tolerance_testing_20240515/Emporia_Results_Extended_20240514005214.csv", skiprows=1, delimiter=",", dtype=str,
               unpack=True)

_, name_0514_1core, _, _, time_diff1_0514_1core, \
 avg_pwr1_0514_1core, avg_pwr_base_0514_1core, total_solves_0514_1core, avg_resid_norm_0514_1core, \
time_single_loop_0514_1core, energy_one_solve_0514_1core, _, _, _, _ = \
    np.loadtxt("tolerance_testing_20240515/Emporia_Results_Extended_20240514113546.csv", skiprows=1, delimiter=",", dtype=str,
               unpack=True)

energy_one_solve_0314_8cores = [float(i) for i in energy_one_solve_0314_8cores]
# print(energy_one_solve)
time_single_loop_0314_8cores = [float(i) for i in time_single_loop_0314_8cores]

energy_one_solve_0510_1core = [float(i) for i in energy_one_solve_0510_1core]
# print(energy_one_solve)
time_single_loop_0510_1core = [float(i) for i in time_single_loop_0510_1core]

energy_one_solve_0514_8cores = [float(i) for i in energy_one_solve_0514_8cores]
# print(energy_one_solve)
time_single_loop_0514_8cores = [float(i) for i in time_single_loop_0514_8cores]

energy_one_solve_0514_1core = [float(i) for i in energy_one_solve_0514_1core]
# print(energy_one_solve)
time_single_loop_0514_1core = [float(i) for i in time_single_loop_0514_1core]

plt.scatter(time_single_loop_0314_8cores, energy_one_solve_0314_8cores, label="8 cores old code")
# plt.scatter(time_single_loop_0510_1core, energy_one_solve_0510_1core, label="1 core first run")
plt.scatter(time_single_loop_0514_8cores, energy_one_solve_0514_8cores, label="8 cores new code")
# plt.scatter(time_single_loop_0514_1core, energy_one_solve_0514_1core, label="1 core second run")
plt.title("Time v.s. Energy Plot")
plt.xlabel("Seconds Single Loop")
plt.ylabel("Energy Single Loop")
plt.legend()
for (s, i, j) in zip(name_0314_8cores, time_single_loop_0314_8cores, energy_one_solve_0314_8cores):
    plt.text(i, j, f"{s}", fontsize=20)
# for (l, m, n) in zip(name_0510_1core, time_single_loop_0510_1core, energy_one_solve_0510_1core):
#     plt.text(m, n, f"{l}", fontsize=20)
for (o, p, q) in zip(name_0514_8cores, time_single_loop_0514_8cores, energy_one_solve_0514_8cores):
    plt.text(p, q, f"{o}", fontsize=20)
# for (z, x, y) in zip(name_0514_1core, time_single_loop_0514_1core, energy_one_solve_0514_1core):
#     plt.text(x, y, f"{z}", fontsize=20)
plt.figure()

plt.show()
