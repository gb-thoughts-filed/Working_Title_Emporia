import csv
import numpy as np
import time
import datetime
import Emporia_Analysis
# Establish Analysis file

t_analysis_file = datetime.now()
t_analysis_file_str = t_analysis_file.strftime("%Y%m%d%H%M%S")
with open(f'Emporia_Analysis_Folder/Emporia_Results_Extended_{t_analysis_file_str}.csv',
          'w', newline='') as file:
    writer = csv.writer(file)
    field = ["python file name",
             "solver name",
             "start time",
             "end time",
             "time difference (s)"
             "avg power (W)",
             "avg power - base (W)",
             "# of loops",
             "avg resid norm",
             "seconds in single loop",
             "energy one solve (J)",
             "tolerance",
             "max iterations",
             "residual count limit",
             "machine information",
             "mesh filename",
             "uk2 vector"]

    writer.writerow(field)

file.close()

count_file_list = []
power_f = []

with open(f'Emporia_Analysis_Folder/Emporia_Results_Extended_{t_analysis_file_str}.csv',
          'a', newline='') as file:
    writer = csv.writer(file)

'''
    writer.writerow([file_name, name, s, e, time_difference_seconds,
                     avg_powers_reduced_W,
                     avg_powers_reduced_minus_base_W,
                     num_loops, avg_resid_norm,
                     seconds_one_loop, energy_one_solve,
                     tol, max_iter, resid_count_lim, machine_info])
'''
