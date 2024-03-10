import csv

with open('Emporia_Analysis_Folder/Emporia_Results_Extended.csv', 'w', newline='') as file:
    writer = csv.writer(file)


    writer.writerow(field)
