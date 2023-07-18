import glob
import subprocess
from pymongo import MongoClient

mongotool = input("Inserire la stringa di connessione di mongoDB: ")
client = mo


for file in files:
    commands = [mongotool + "\\mongoimport", "--type", "csv",
                "--fields", "timestamp,id_street,vehicles,average_speed",
                "--db", mydatabase,
                "--collection", file[:-4],
                "--file", dir_path + "\\" + file,
                "--numInsertionWorkers", "4"]
    subprocess.Popen(commands, shell=True)
