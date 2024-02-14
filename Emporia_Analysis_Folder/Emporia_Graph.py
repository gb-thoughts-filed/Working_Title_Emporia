import numpy as np
import matplotlib.pyplot as plt

'''
field = ["python file name",
         "solver name",
         "avg energy - base",
         "# of loops",
         "avg resid norm",
         "seconds in single loop",
         "avg energy in loop",
         "time in fx, profiler"]
'''

txt_file, name, eminusb, numloops, avgresidnorm, sec1loop, e1loop, tinfx = \
np.loadtxt("Emporia_Results.csv", skiprows=1, delimiter=",", dtype=str, unpack=True)

e1loop = [float(i) for i in e1loop]
sec1loop = [float(i) for i in sec1loop]
avgresidnorm = [float(i) for i in avgresidnorm]

fig = plt.figure()

depth_plt = fig.add_subplot(projection='3d')
depth_plt.scatter(sec1loop, e1loop, avgresidnorm, marker="x")
depth_plt.set_xlabel("Seconds in Loop", wrap=True)
depth_plt.set_ylabel("Energy Minus Base in a Single Loop", wrap=True)
depth_plt.set_zlabel("Average Residual Norm", wrap=True)
for (s, i, j, k) in zip(name, sec1loop, e1loop, avgresidnorm):
    depth_plt.text(i, j, k, f"{s}")
plt.show()
