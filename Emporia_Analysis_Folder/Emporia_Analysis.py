import csv
import numpy as np
import time
import datetime



# important attributes

base_energy_W = 82.4

# Count Data Text File Created in Function


def count_data_extraction(file):

    # ensures that only the last line of the txt files generated with python
    # programs is read
    count_data_file = open(file)
    row_num = len(count_data_file.readlines())
    index = row_num -1
    count_data_file.close()
    count_data_file = open(file)
    count_data = count_data_file.readlines()[index].split(",")
    # print(count_data)
    # actual data is extracted from the txt files here
    num_loops = int(count_data[1])
    avg_resid_norm = float(count_data[3])
    file_name = file
    name = count_data[4]
    start = count_data[0]
    end = count_data[2]
    tol = count_data[5]
    max_iter = count_data[6]
    resid_count_lim = count_data[7]
    machine_info = count_data[8]
    mesh_f = count_data[9]
    uk2 = count_data[10]
    return start, end, num_loops, \
           avg_resid_norm, file_name, name, tol, \
           max_iter, resid_count_lim, machine_info, mesh_f, uk2


def date_processing(start_time, end_time):

    # python's datetime format didn't match the format given by the emporia plug
    # so this is data cleaning to make sure the dates match up.
    # Specifically the numbers after the decimal point for python's datetime is
    # removed here.
    c_strt_time = start_time.strip().split(".")
    c_strt_time = c_strt_time[0].strip()
    c_end_time = end_time.strip().split(".")
    c_end_time = c_end_time[0].strip()
    print(c_strt_time)
    # Here the newly formatted start and end times are turned into time objects
    c_iso_strt_time = datetime.datetime.strptime(c_strt_time, "%Y-%m-%d %H:%M:%S")
    c_iso_end_time = datetime.datetime.strptime(c_end_time, "%Y-%m-%d %H:%M:%S")
    print(c_iso_strt_time)
    print(c_iso_end_time)
    c_iso_strt_time = c_iso_strt_time + datetime.timedelta(minutes=5)
    c_iso_end_time = c_iso_end_time - datetime.timedelta(minutes=5)
    print(c_iso_strt_time)
    print(c_iso_end_time)

    time_difference = c_iso_end_time - c_iso_strt_time
    print(time_difference.seconds)

    return c_iso_strt_time, c_iso_end_time, time_difference.seconds


# Time objects given by the text files are compared to time objects created from
# the Emporia energy data csv.
def date_match(date_lst, date):

    for i in np.arange(len(date_lst)):
        i_struct = time.strptime(date_lst[i], "%m/%d/%Y %H:%M:%S")
        if i_struct[0:5] == date[0:5]:
            return i


# The needed powers are extracted from the Emporia energy data csv

def needed_powers(power_lst, start_i, end_i):
    powers = []
    for index in np.arange(len(power_lst)):
        if start_i <= index <= end_i:
            powers.append(float(power_lst[index]))

    return powers


def energy_count_extraction(energy_file, count_file):

    s, e, num_loops, avg_resid_norm, file_name, \
    name, tol, max_iter, resid_count_lim, machine_info, \
    meshfile, uk2_vector = count_data_extraction(
        count_file)

    c_iso_strt_time, c_iso_end_time, time_difference_seconds = date_processing(s, e)

    #Power CSV retreived from Emporia site

    power_data_dates, powers = np.loadtxt(
        energy_file,
        skiprows=1, delimiter=",", dtype=str, unpack=True)

    start_index = date_match(power_data_dates, c_iso_strt_time)
    end_index = date_match(power_data_dates, c_iso_end_time)

    print(start_index, end_index)

    powers_reduced = needed_powers(powers, start_index, end_index)
    # print(powers_reduced)

    return s, e, num_loops, avg_resid_norm, file_name, \
           name, tol, max_iter, resid_count_lim, machine_info, meshfile, \
           uk2_vector, time_difference_seconds, powers_reduced

def calculations(reduced_pwr_lst, total_seconds, number_loops, base_energy_W):
    # Energies by Emporia are reported in terms of W, the below line
    # averages the powers and changes it to Wh by multiplying by 1000.
    avg_powers_reduced_W = np.average(reduced_pwr_lst) * 1000

    avg_powers_reduced_minus_base_W = avg_powers_reduced_W - base_energy_W

    seconds_one_loop = total_seconds / number_loops

    energy_one_solve = avg_powers_reduced_minus_base_W * seconds_one_loop

    return avg_powers_reduced_W, avg_powers_reduced_minus_base_W, \
           seconds_one_loop, energy_one_solve




