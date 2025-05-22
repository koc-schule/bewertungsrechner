"""
Beschreibung
"""


def results_csv_file_to_object(csv_name: str) -> None:
    results = []
    file = open(csv_name, "r")
    file.read()
    for i in range(0, len(file)):
        row = file.readline(i)
        row = remove_unimportant_data(row)
        results.append({
            row[:row.index(",")]: row[row.index(",") + 1:]
        })
    print(results)


def remove_unimportant_data(row: str) -> str:
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

results_csv_file_to_object("quiz_13965756.csv")