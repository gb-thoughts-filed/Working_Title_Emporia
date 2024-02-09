import csv
import numpy as np
import time

#important attributes

base_energy_Wh = 82.4

#Count Data Text File Created in Function

def count_data_extraction(file, solver_name):

    count_data_file = open(file)
    row_num = len(count_data_file.readlines())
    index = row_num -1
    count_data_file.close()
    count_data_file = open(file)
    count_data = count_data_file.readlines()[index].split(",")
    #print(count_data)
    num_loops = int(count_data[1])
    avg_resid_norm = 0 #int(count_data[3])
    file_name = file
    name = solver_name
    start = count_data[0]
    end = count_data[2]
    return start, end, num_loops, avg_resid_norm, file_name, name

s, e, num_loops, avg_resid_norm, file_name, name =  count_data_extraction("scipy_sparse_linalg_lgmres January062024.txt", "lgmres")
c_strt_time = s.strip().split(".")
c_strt_time = c_strt_time[0].strip()
c_end_time = e.strip().split(".")
c_end_time = c_end_time[0].strip()
print(c_strt_time)

c_iso_strt_time = time.strptime(c_strt_time, "%Y-%m-%d %H:%M:%S")
c_iso_end_time = time.strptime(c_end_time, "%Y-%m-%d %H:%M:%S")
print(c_iso_strt_time[3])
print(c_iso_end_time[3])



#Energy CSV retreived from Emporia site

energy_data_dates, energies = np.loadtxt("343254-emporiaplug1-1MINJan6_7.csv",
                         skiprows=1, delimiter=",", dtype=str, unpack=True)

def date_match(date_lst, date):

    for i in np.arange(len(date_lst)):
        i_struct = time.strptime(date_lst[i], "%m/%d/%Y %H:%M:%S")
        if i_struct[0:5] == date[0:5]:
            return i

start_index = date_match(energy_data_dates, c_iso_strt_time)
end_index = date_match(energy_data_dates, c_iso_end_time)

print(start_index, end_index)

def needed_energies(energy_lst, start_i, end_i):
    energies = []
    for index in np.arange(len(energy_lst)):
        if start_i <= index <= end_i:
            energies.append(float(energy_lst[index]))

    return energies

energies_reduced = needed_energies(energies, start_index, end_index)
#print(energies_reduced)
avg_energies_reduced_Wh = np.average(energies_reduced)*1000

avg_energies_reduced_minus_base = avg_energies_reduced_Wh - base_energy_Wh

energy_one_loop = avg_energies_reduced_minus_base / num_loops

seconds_one_loop = 3600 / num_loops


with open('Emporia_Results.csv', 'a', newline='') as file:
    writer = csv.writer(file)

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

    writer.writerow([file_name, name, avg_energies_reduced_minus_base,
                     num_loops, avg_resid_norm,
                     seconds_one_loop, energy_one_loop, 0])


