import csv

with open('Emporia_Analysis_Folder/Emporia_Results_Extended.csv', 'w', newline='') as file:
    writer = csv.writer(file)
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

    writer.writerow(field)
