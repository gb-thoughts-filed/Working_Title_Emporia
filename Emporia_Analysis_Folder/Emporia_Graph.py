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
print(e1loop)
sec1loop = [float(i) for i in sec1loop]
print(sec1loop)
avgresidnorm = [float(i) for i in avgresidnorm]
print(avgresidnorm)


plt.scatter(np.log(sec1loop), np.log(e1loop))
plt.title("Time v.s. Energy Log Plot")
plt.xlabel("Seconds Single Loop")
plt.ylabel("Energy Single Loop")
for (s, i, j) in zip(name, np.log(sec1loop), np.log(e1loop)):
    plt.text(i, j, f"{s}", fontsize=20)
plt.figure()

plt.show()
