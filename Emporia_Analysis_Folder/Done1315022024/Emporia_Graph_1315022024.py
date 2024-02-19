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
np.loadtxt("../Emporia_Results.csv", skiprows=1, delimiter=",", dtype=str, unpack=True)

e1loop = [float(i) for i in e1loop]
print(e1loop)
sec1loop = [float(i) for i in sec1loop]
print(sec1loop)
avgresidnorm = [float(i) for i in avgresidnorm]
print(avgresidnorm)

fig = plt.figure()

depth_plt = fig.add_subplot(projection='3d')
depth_plt.scatter(np.log(sec1loop), np.log(e1loop), np.log(avgresidnorm), marker=".", s=100)
depth_plt.set_title("Time v.s. Energy v.s. Average Residual Norm")
depth_plt.set_xlabel("Seconds in Loop", wrap=True)
depth_plt.set_ylabel("Energy Minus Base in a Single Loop (Wh)", wrap=True)
depth_plt.set_zlabel("Average Residual Norm", wrap=True)

for (s, i, j, k) in zip(name, np.log(sec1loop), np.log(e1loop), np.log(avgresidnorm)):
    depth_plt.text(i, j, k, f"{s}", fontsize=5)

plt.figure()

plt.scatter(np.log(sec1loop), np.log(e1loop))
plt.title("Time v.s. Energy")
plt.xlabel("Seconds Single Loop")
plt.ylabel("Energy Single Loop")
for (s, i, j) in zip(name, np.log(sec1loop), np.log(e1loop)):
    plt.text(i, j, f"{s}", fontsize=20)
plt.figure()

plt.scatter(np.log(sec1loop), np.log(avgresidnorm))
plt.title("Time v.s. Average Residual Norm")
plt.xlabel("Seconds Single Loop")
plt.ylabel("Average Residual Norm")
for (s, i, j) in zip(name, np.log(sec1loop), np.log(avgresidnorm)):
    plt.text(i, j, f"{s}", fontsize=20)
plt.figure()

plt.scatter(np.log(e1loop), np.log(avgresidnorm))
plt.title("Energy v.s. Average Residual Norm")
plt.xlabel("Energy Single Loop")
plt.ylabel("Average Residual Norm")
for (s, i, j) in zip(name, np.log(e1loop), np.log(avgresidnorm)):
    plt.text(i, j, f"{s}", fontsize=20)
plt.figure()

plt.show()
