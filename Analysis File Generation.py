import csv

with open('Emporia_Analysis_Folder/Emporia_Results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["python file name",
             "solver name",
             "avg energy - base",
             "# of loops",
             "avg resid norm",
             "seconds in single loop",
             "avg energy in loop",
             "time in fx, profiler"]

    writer.writerow(field)
