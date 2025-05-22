"""
Aus einer .csv-Datei werden Ergebnisse herausgelesen und in einer list[dict] zurückgegeben
"""


def results_csv_file_to_object(csv_name: str) -> list[dict]:
    """erstellt eine Liste, in der dictionaries gespeichert werden, die die ergebnisse enthalten"""
    results = []
    file = open(csv_name, "r")
    i = 1
    while True:
        try:
            row = file.readline()
            row = remove_unimportant_data(row)
            results.append({
                row[:row.index(",")].replace("ï»¿", ""): row[row.index(",") + 1:].replace("\n", "")
            })
            i += 1
        except:
            break

    return results


def remove_unimportant_data(row: str) -> str:
    """löscht aus einer Zeile der Ergebnisse unnötige Daten heraus: starttime, endtime, time"""
    counter = 0
    for i in range(len(row)):
        if row[i] == ",":
            counter += 1
        if counter == 1:
            start_index = i
            counter += 1
        elif counter == 5:
            row = row[:start_index] + row[i:]
            return row

print(results_csv_file_to_object("quiz_13965756.csv"))