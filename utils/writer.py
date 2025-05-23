"""importieren der Result-Klasse aus dem parent-directory"""
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import Result

def write_to_csv(result:Result)->None:

   """ Schreibt ein Result- Objekt in eine .csv-Datei um 
       Argumente: result: Result
   """

   """Auswählen der Datei"""
   filename  = "./csv_files/" + str((result.get_exam()).exam_name) + ".csv"
   file = open(filename,"w")

   """Erstellen der ersten Zeile der csv_datei (Spaltennamen)"""
   task_names_list = list(((result.get_exam()).tasks).keys())
   task_names = ""
   for key in task_names_list:
       task_names = task_names + str(key) + ", "
   column_name = "Name, Date, Percent, Points Earned, Points Possible, "  + task_names + "\n"
   file.write(column_names)

   """Eintragen der Ergebnisse für jeden Schüler"""
   for student in result.results:

       """gleichbleibende Einträge in Variablen speichern """
       student_name = student["name"] + ","
       exam_date = str(result.get_date()) + ","
       percentage_earned = str(student["percentage_earned"]) + ","
       points_earned = str(student["points_earned"]) + "," 
       max_points = str((result.get_exam()).max_points) + ","
       studentdata = student_name + exam_date + percentage_earned + points_earned + max_points 

       """Speichern der Punktzahlen je Aufgabe für einen Schüler """
       for task in list(((result.get_exam()).tasks).keys()):
           studentdata = studentdata + str(student[task]) + ","
       studentdata = studentdata + "\n"

       file.write(studentdata)       
