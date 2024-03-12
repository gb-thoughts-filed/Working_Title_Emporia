import csv
from datetime import datetime
from dataclasses import dataclass
import platform
import numpy as np
import os

RESULT_FILE_HEADERS = {"python file name",
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
                       "uk vector"}

@dataclass
class SolverReturnedData:
    start_time: datetime
    end_time: datetime
    total_solves: int
    average_residual_norm: str
    solver_name: str
    solver_tolerance: str
    max_iterations: str
    residual_norm_average_list_limit: str
    machine_info: str
    mesh_filename: str
    uk_vector: str


def solver_returned_data_contents(file):
    with open(file) as solver_data_contents:
        return solver_data_contents.readlines()[-1].split(",")

def string_to_datetime(time: str) -> datetime:
    time_split_decimal_pt = time.strip().split(".")
    time_split_decimal_pt = time_split_decimal_pt[0].strip()
    time_datetime_object = datetime.strptime(time_split_decimal_pt, "%Y-%m-%d %H:%M:%S")
    return time_datetime_object

def parse_solver_returned_data_contents(solver_returned_data_contents:list
                                        )-> SolverReturnedData:
    POWER_WARMUP_RAMP = 5

    start_time = string_to_datetime(solver_returned_data_contents[0]) + \
        datetime.timedelta(minutes=POWER_WARMUP_RAMP)
    end_time = string_to_datetime(solver_returned_data_contents[2]) - \
        datetime.timedelta(minutes=POWER_WARMUP_RAMP)
    number_of_loops = int(solver_returned_data_contents[1])

    return SolverReturnedData(start_time, end_time, number_of_loops,
                              solver_returned_data_contents[3],
                              solver_returned_data_contents[4],
                              solver_returned_data_contents[5],
                              solver_returned_data_contents[6],
                              solver_returned_data_contents[7],
                              solver_returned_data_contents[8],
                              solver_returned_data_contents[9],
                              solver_returned_data_contents[10])

def date_match(date_lst: list, date: datetime) -> int:

    for i in np.arange(len(date_lst)):
        i_datetime_object = datetime.strptime(date_lst[i], "%m/%d/%Y %H:%M:%S")
        if i_datetime_object[0:5] == date[0:5]:
            return i

def needed_powers(power_lst: list, start_i: int, end_i: int) -> list:
    powers = []
    for index in np.arange(len(power_lst)):
        if start_i <= index <= end_i:
            powers.append(float(power_lst[index]))

    return powers

def write_results(file: str, results: list, headers: list = None):
    to_write = []
    if not os.path.exists(file):
        to_write.append(headers or RESULT_FILE_HEADERS)
        '''
        with open(file, 'w'):
            writer = csv.writer(file)
            writer.writerow(headers or RESULT_FILE_HEADERS)
           '''
    with open(file,'a', newline='') as f:
        to_write.append(results)
        writer = csv.writer(file)
        writer.writerows(to_write)




if __name__ == "__main__":

    BASE_ENERGY_W = 82.4

    file_path = "meshes_octopus_mesh__sf_obj_20240310201806/bicg_March102024.txt"

    power_data_dates, powers = np.loadtxt(
        "energy_file",
        skiprows=1, delimiter=",", dtype=str, unpack=True)

    start_index = date_match(power_data_dates, SolverReturnedData.start_time)
    end_index = date_match(power_data_dates, SolverReturnedData.end_time)

    powers_list_reduced = needed_powers(powers, start_index, end_index)

    avg_powers_reduced_W = np.average(powers_list_reduced) * 1000

    avg_powers_reduced_minus_base_W = avg_powers_reduced_W - BASE_ENERGY_W
    time_difference_seconds = (SolverReturnedData.end_time -
                               SolverReturnedData.start_time).seconds
    seconds_one_loop = time_difference_seconds / SolverReturnedData.total_solves

    energy_one_solve = avg_powers_reduced_minus_base_W * seconds_one_loop

    time_analysis_file_str = datetime.now().strftime("%Y%m%d%H%M%S")

    analysis_file_name = f'Emporia_Analysis_Folder/' \
                         f'Emporia_Results_Extended_{time_analysis_file_str}.csv'

    total_results = [file_path,
                     SolverReturnedData.solver_name,
                     SolverReturnedData.start_time,
                     SolverReturnedData.end_time,
                     time_difference_seconds,
                     avg_powers_reduced_W,
                     avg_powers_reduced_minus_base_W,
                     SolverReturnedData.total_solves,
                     SolverReturnedData.average_residual_norm,
                     seconds_one_loop,
                     energy_one_solve,
                     SolverReturnedData.solver_tolerance,
                     SolverReturnedData.max_iterations,
                     SolverReturnedData.residual_norm_average_list_limit,
                     SolverReturnedData.machine_info,
                     SolverReturnedData.mesh_filename,
                     SolverReturnedData.uk_vector]

    write_results(analysis_file_name, total_results, RESULT_FILE_HEADERS)
