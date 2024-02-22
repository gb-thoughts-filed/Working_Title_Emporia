import csv
import numpy as np
import time

#important attributes

base_energy_Wh = 82.4

#Count Data Text File Created in Function

def count_data_extraction(file, solver_name):

    #ensures that only the last line of the txt files generated with python
    #programs is read
    count_data_file = open(file)
    row_num = len(count_data_file.readlines())
    index = row_num -1
    count_data_file.close()
    count_data_file = open(file)
    count_data = count_data_file.readlines()[index].split(",")
    #print(count_data)
    #actual data is extracted from the txt files here
    num_loops = int(count_data[1])
    avg_resid_norm = float(count_data[3])
    file_name = file
    name = solver_name
    start = count_data[0]
    end = count_data[2]
    return start, end, num_loops, avg_resid_norm, file_name, name

s, e, num_loops, avg_resid_norm, file_name, name =  count_data_extraction(
    "Done181920022024/sparse_linalg_spsolve February202024.txt", "scipy spsolve")

#python's datetime format didn't match the format given by the emporia plug
#so this is data cleaning to make sure the dates match up.
#Specifically the numbers after the decimal point for python's datetime is
#removed here.
c_strt_time = s.strip().split(".")
c_strt_time = c_strt_time[0].strip()
c_end_time = e.strip().split(".")
c_end_time = c_end_time[0].strip()
print(c_strt_time)
#Here the newly formatted start and end times are turned into time objects
c_iso_strt_time = time.strptime(c_strt_time, "%Y-%m-%d %H:%M:%S")
c_iso_end_time = time.strptime(c_end_time, "%Y-%m-%d %H:%M:%S")
print(c_iso_strt_time[3])
print(c_iso_end_time[3])



#Energy CSV retreived from Emporia site

energy_data_dates, energies = np.loadtxt(
    "343254-emporiaplug1-1MIN181920.csv",
    skiprows=1, delimiter=",", dtype=str, unpack=True)

#Time objects given by the text files are compared to time objects created from
#the Emporia energy data csv.
def date_match(date_lst, date):

    for i in np.arange(len(date_lst)):
        i_struct = time.strptime(date_lst[i], "%m/%d/%Y %H:%M:%S")
        if i_struct[0:5] == date[0:5]:
            return i

start_index = date_match(energy_data_dates, c_iso_strt_time)
end_index = date_match(energy_data_dates, c_iso_end_time)

print(start_index, end_index)

#The needed energies are extracted from the Emporia energy data csv
def needed_energies(energy_lst, start_i, end_i):
    energies = []
    for index in np.arange(len(energy_lst)):
        if start_i <= index <= end_i:
            energies.append(float(energy_lst[index]))

    return energies

energies_reduced = needed_energies(energies, start_index, end_index)
#print(energies_reduced)

#Energies by Emporia are reported in terms of Kwh, the below line
#averages the energies and changes it to Wh by multiplying by 1000.
avg_energies_reduced_Wh = np.average(energies_reduced)*1000

avg_energies_reduced_minus_base = avg_energies_reduced_Wh - base_energy_Wh

energy_one_loop = avg_energies_reduced_minus_base / num_loops

seconds_one_loop = 3600 / num_loops


with open('Emporia_Results_Extended.csv', 'a', newline='') as file:
    writer = csv.writer(file)

    '''
    field = ["python file name",
             "solver name",
             "start time",
             "end time",
             "avg energy",
             "avg energy - base",
             "# of loops",
             "avg resid norm",
             "seconds in single loop",
             "avg energy in loop"]
    '''

    writer.writerow([file_name, name, s, e, avg_energies_reduced_Wh,
                     avg_energies_reduced_minus_base,
                     num_loops, avg_resid_norm,
                     seconds_one_loop, energy_one_loop])



