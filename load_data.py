import glob
import subprocess

mongotool = input("Inserire percorso mongoimport: ")
dir_path = input("Inserire percorso dei file csv: ")


mydatabase = "detections"
files = glob.glob1(dir_path, "*.csv")


for file in files:
    commands = [mongotool + "\\mongoimport", "--type", "csv",
                "--fields", "timestamp,id_street,vehicles,average_speed",
                "--db", mydatabase,
                "--collection", file[:-4],
                "--file", dir_path + "\\" + file,
                "--numInsertionWorkers", "4"]
    subprocess.Popen(commands, shell=True)
